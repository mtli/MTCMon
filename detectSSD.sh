#!/bin/bash

INPUT_PATH=$1

PARTITION_NAME=`df "$INPUT_PATH" | tail -n1 | awk '{print $1}'`
DEVICE_NAME=`python partition2disk.py $PARTITION_NAME`
IS_SSD=`cat /sys/block/$DEVICE_NAME/queue/rotational`
((IS_SSD ^= 1))
echo $IS_SSD
