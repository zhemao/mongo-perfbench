#!/bin/bash

# stop background noise processes on servers specified in hosts file

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
