#!/bin/bash

# This script runs the javascript benchmarks in a loop
# The number of threads used on each run iterate from 1 to $MAXTHREADS
# After finishing the loop, the results will be dumped to ~/results.json

if [ -z $6 ]; then
    echo "Usage: $0 user@results-server user@mongod-server operation numthreads increment suite" 
    exit 1
fi

RESULTS_SERVER=$1
MONGO_SERVER=$2
OPERATION=$3
MAXTHREADS=$4
INCREMENT=$5
SUITE=$6

source "$(dirname $0)/pbrc.sh"

# cd into the mongo repository
cd "$MONGO_DIR"

SERVER_INFO=$(ssh $MONGO_SERVER '~/mongo/perfbench/getserverinfo.sh')

for (( i=$INCREMENT; i<=$MAXTHREADS; i+=$INCREMENT )); do
    ssh $MONGO_SERVER '~/mongo/perfbench/cleanandrestart.sh'
    # wait until port 27017 on server is open
    while ! nc -z $MONGO_SERVER 27017 ; do sleep 1 ; done
    echo "Load testing with $i threads"
    configstr="globalExtraOption = {numThreads: $i, databaseURL: \"$MONGO_SERVER\", \
                testServerInfo: $SERVER_INFO}; suiteName = \"$SUITE\";"

    mongo --eval "$configstr" $RESULTS_SERVER perfbench/$OPERATION.js
done

