#!/bin/bash

THIS_FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

. $THIS_FILE_DIR/kill_monitor.sh

# select input device 10 to prevent conflicting with ssh
while read -u10 NODE_NAME; do
	ssh $NODE_NAME bash "$THIS_FILE_DIR/run_single_node.sh" $NODE_NAME "/project_data/mtcmon/nodestats/"
done 10< "$THIS_FILE_DIR/node-list.txt"