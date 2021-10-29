from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import time
import collections
import subprocess
import io # for python2.7

import psutil
import jinja2
from pynvml import *

from humanize_time import humanize_time

REFRESH_SEC = 15

# take n snapshots and then take the max/min/avg 
NSNAPSHOT = 5
SNAPSHOT_INTERVAL_SEC = 1

toGB = lambda x: int(round(x / 2**30))
toMB = lambda x: int(round(x / 2**20))
# add "int" since in Python 2 "round" returns a float instead of int

thisfiledir = os.path.dirname(os.path.realpath(__file__))

def is_ssd(path):
    return subprocess \
        .check_output(['sh', os.path.join(thisfiledir, 'detectSSD.sh'), path]) \
        .decode('utf-8')[0] == '1'
        
def getprocinfo(pid):
    P = psutil.Process(pid)
    cmd = P.name() or '<unknown>'
    user = P.username() or '<unknown>'
    runtime = humanize_time(time.time() - P.create_time())
    return (user, cmd, runtime)

if __name__ == "__main__":
    machine_name = sys.argv[1]
    outdir = sys.argv[2]

    # prevent race condition
    try:
        os.makedirs(outdir)
    except OSError as e:
        # 17: File exists
        if e.errno != 17:
            raise e

    nvmlInit()
    deviceCount = nvmlDeviceGetCount()
    gpudata = [{} for i in range(deviceCount)]

    with io.open(os.path.join(
        thisfiledir, 'templates', 'section.html'), encoding='utf-8') as fin:
        template = jinja2.Template(fin.read())

    while True:
        # Getting data with a single snapshot
        sysdata = {}
        sysdata['cores'] = psutil.cpu_count(logical=False)
        sysdata['threads'] = psutil.cpu_count()
        sysdata['mem_total'] = toGB(psutil.virtual_memory().total)
        sysdata['swap_total'] = toGB(psutil.swap_memory().total)
        sysdata['scratch_type'] = 'SSD' # if is_ssd('/scratch') else 'HDD'
        # is_ssd doesn't work on Autobot
        scratch_usage = psutil.disk_usage('/scratch')
        sysdata['scratch_used'] = toGB(scratch_usage.used)
        sysdata['scratch_total'] = toGB(scratch_usage.total)

        if os.path.isdir('/ssd0'):
            ssd0_usage = psutil.disk_usage('/ssd0')
            sysdata['ssd0_exist'] = True
            sysdata['ssd0_used'] = toGB(ssd0_usage.used)
            sysdata['ssd0_total'] = toGB(ssd0_usage.total)
        else:
            sysdata['ssd0_exist'] = False

        if os.path.isdir('/ssd1'):
            ssd1_usage = psutil.disk_usage('/ssd1')
            sysdata['ssd1_exist'] = True
            sysdata['ssd1_used'] = toGB(ssd1_usage.used)
            sysdata['ssd1_total'] = toGB(ssd1_usage.total)
        else:
            sysdata['ssd1_exist'] = False

        procs = []
        gpu_error = [False]*deviceCount
        for i in range(deviceCount):
            try:
                handle = nvmlDeviceGetHandleByIndex(i)
                name = nvmlDeviceGetName(handle)
                gpudata[i]['name'] = name.decode('utf-8')

                memInfo = nvmlDeviceGetMemoryInfo(handle)
                gpudata[i]['mem_free'] = toMB(memInfo.total - memInfo.used)
                gpudata[i]['mem_total'] = toMB(memInfo.total)
                gpudata[i]['mem_usage'] = memInfo.used/memInfo.total*100

                procs.append(nvmlDeviceGetComputeRunningProcesses(handle))
                gpudata[i]['procs'] = [(p.pid, ) + getprocinfo(p.pid) for p in procs[i]]
            except Exception as e:
                gpu_error[i] = True
                print('Unable to access GPU device (id: %d)' % i)
                print(e)
                gpudata[i]['name'] = str(e)
                gpudata[i]['mem_free'] = 'N/A'
                gpudata[i]['mem_total'] = 0
                gpudata[i]['mem_usage'] = 0
                gpudata[i]['procs'] = []

        # Getting data by combining multiple snapshots
        cpu_usage = [None]*NSNAPSHOT
        mem_usage = [None]*NSNAPSHOT
        swap_usage = [None]*NSNAPSHOT
        disk_read = [None]*NSNAPSHOT
        disk_write = [None]*NSNAPSHOT

        gpu_mem = [ [[None]*NSNAPSHOT for p in d] for d in procs ]
        for t in range(NSNAPSHOT):
            cpu_usage[t] = psutil.cpu_percent()
            mem_usage[t] = psutil.virtual_memory().percent
            swap_usage[t] = psutil.swap_memory().percent
            diskio = psutil.disk_io_counters()
            disk_read[t] = diskio.read_bytes
            disk_write[t] = diskio.write_bytes
            # only the difference matters
            if t > 0:
                disk_read[t-1] = disk_read[t] - disk_read[t-1]
                disk_write[t-1] = disk_write[t] - disk_write[t-1]

            for i in range(deviceCount):
                if gpu_error[i]:
                    continue
                try:
                    for j in range(len(procs[i])):
                        gpu_mem[i][j][t] = procs[i][j].usedGpuMemory
                except Exception as e:
                    gpu_error[i] = True
                    print('Unable to access GPU device (id: %d)' % i)
                    print(e)
                    gpudata[i]['name'] = str(e)
                    gpudata[i]['mem_free'] = 'N/A'
                    gpudata[i]['mem_total'] = 0
                    gpudata[i]['mem_usage'] = 0
                    gpudata[i]['procs'] = []
            time.sleep(SNAPSHOT_INTERVAL_SEC)

        sysdata['cpu_usage'] = max(cpu_usage)
        sysdata['mem_usage'] = max(mem_usage)
        sysdata['swap_usage'] = max(swap_usage)
        sysdata['disk_read'] = toMB(max(disk_read[0:-1]))
        sysdata['disk_write'] = toMB(max(disk_write[0:-1]))

        for i in range(deviceCount):
            if gpu_error[i]:
                continue
            for j in range(len(procs[i])):
                gpudata[i]['procs'][j] += (toMB(max(gpu_mem[i][j])), )

            # Update 2021 for new NVIDIA driver (455.38)
            # Filtering out zero-memory processes
            gpudata[i]['procs'] = [p for p in gpudata[i]['procs'] if p[-1]]
            
        res = template.render(machine_name=machine_name,
                            update_time=time.strftime("%m-%d-%Y %H:%M:%S %Z"),
                            gpudata=gpudata,
                            sysdata=sysdata)
        with io.open(os.path.join(outdir, machine_name + '.html'), 'w', encoding='utf8') as fout:
            fout.write(res)
        time.sleep(REFRESH_SEC)
