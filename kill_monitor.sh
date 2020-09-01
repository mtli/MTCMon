#!/bin/bash

SCRIPT_NAME=getstat.py

THIS_FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

# select input device 10 to prevent conflicting with ssh
while read -u10 NODE_NAME; do
	ssh $NODE_NAME bash "$THIS_FILE_DIR/kill_single_node.sh" "$THIS_FILE_DIR/$SCRIPT_NAME" $NODE_NAME
done 10< "$THIS_FILE_DIR/node-list.txt"
