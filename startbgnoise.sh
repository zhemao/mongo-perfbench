#!/bin/bash

# Run holdit.sh on the hosts specified in the hosts file
# Hosts file syntax is the same as for runbench.sh

if [ -z "$1" ]; then
    echo "Must specify configuration file"
    exit 1
fi

HOSTS_FILE=$1

RESULTS_SERVER=$(head -n 1 $HOSTS_FILE)
MONGOD_SERVER=$(head -n 2 $HOSTS_FILE | tail -n 1)

tail -n +3 $HOSTS_FILE | while read host operation threads; do
    echo "$host -> $MONGOD_SERVER"
    ssh -n $host "nohup ~/mongo/perfbench/holdit.sh $RESULTS_SERVER $MONGOD_SERVER \
                    $operation $threads < /dev/null &> ~/holdit.log &" 
    scp $host:holdit.pid $host-holdit.pid
done

