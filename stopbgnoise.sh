#!/bin/bash

# This script starts the benchmarking
# It takes as an argument a file listing the hosts you want to connect to
# The host on the first line is the database server
# The hosts on the remaining lines are the load testing servers

if [ -z "$1" ]; then
    echo "Must specify configuration file"
    exit 1
fi

HOSTS_FILE=$1

tail -n +3 $HOSTS_FILE | while read host operation threads; do
    if [ -f $host-holdit.pid ]; then
        echo "Killing holdit.sh on $host"
        ssh -n $host "kill $(cat $host-holdit.pid) && killall mongo" 
        rm $host-holdit.pid
    fi
done
