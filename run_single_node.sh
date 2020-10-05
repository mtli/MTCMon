#!/bin/bash

# SCRIPT_NAME=getstat.py
# MACHINE_NAME=$1
# OUT_DIR=$2

SCRIPT_NAME=/opt/MTCMon/getstat.py
MACHINE_NAME="$(hostname | cut -d. -f1)"
OUT_DIR=/project_data/mtcmon/nodestats

nohup python "$SCRIPT_NAME" $MACHINE_NAME $OUT_DIR > /tmp/monitor-$MACHINE_NAME.log 2>&1 &
echo "Started script on $MACHINE_NAME"

