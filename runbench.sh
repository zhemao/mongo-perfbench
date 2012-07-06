#!/bin/bash

# This script starts the benchmarking
# It takes as an argument a file listing the hosts you want to connect to
# The host on the first line is the database server
# The hosts on the remaining lines are the load testing servers

if [ -z "$2" ]; then
    echo "Usage: $0 conffile suitename"
    exit 1
fi

HOSTS_FILE=$1
SUITE=$2

RESULTS_SERVER=$(head -n 1 $HOSTS_FILE)
MONGOD_SERVER=$(head -n 2 $HOSTS_FILE | tail -n 1)

tail -n +3 $HOSTS_FILE | while read host operation threads incr; do
    echo "$host -> $MONGOD_SERVER"
    ssh -n $host "~/mongo/perfbench/rampup.sh $RESULTS_SERVER $MONGOD_SERVER \
                        $operation $threads $incr $SUITE"
    ssh -n $host "nohup ~/mongo/perfbench/holdit.sh $RESULTS_SERVER $MONGOD_SERVER \
                    $operation $threads < /dev/null &> ~/holdit.log &" 
    scp ${host}:holdit.pid $host-holdit.pid
done

tail -n +3 $HOSTS_FILE | while read host operation threads; do
    if [ -f $host-holdit.pid ]; then
        echo "Killing holdit.sh on $host"
        ssh -n $host "kill $(cat $host-holdit.pid) && killall mongo" 
        rm $host-holdit.pid
    fi
done
