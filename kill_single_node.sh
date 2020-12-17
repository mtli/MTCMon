#!/bin/bash

SCRIPT_NAME=$1
MACHINE_NAME=$2

prev_proc=`pgrep -u $(whoami) -af python | grep $SCRIPT_NAME | cut -d' ' -f 1`
if [ -n "$prev_proc" ]; then
  echo "Killing previous procs on $MACHINE_NAME: $prev_proc"
  kill -9 $prev_proc
fi