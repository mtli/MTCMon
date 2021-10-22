'''
Maps the partition name (output of df) to the disk name
listed under /sys/block/
'''

from __future__ import absolute_import
from __future__ import print_function

import sys, string

partition = sys.argv[1]
partition = partition.split('/')[-1]
if partition.startswith('sd'):
    # remove trailing numbers
    disk = partition.rstrip(string.digits)
elif partition.startswith('nvme'):
    # remove trailing 'p' + numbers
    pidx = partition.rfind('p')
    if pidx == -1:
        disk = partition
    else:
        disk = partition[:pidx]
else:
    # unknown partition format
    disk = partition

print(disk)
