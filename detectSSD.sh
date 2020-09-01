#!/bin/bash

INPUT_PATH=$1

DEVICE_NAME=`df "$INPUT_PATH" | tail -n1 | awk '{print $1}' | sed -nE "s/.*\/([a-z]+)[^\/]+$/\1/p"`
IS_SSD=`cat /sys/block/$DEVICE_NAME/queue/rotational`
((IS_SSD ^= 1))
echo $IS_SSD
