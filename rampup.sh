#!/bin/bash

# This script runs the javascript benchmarks in a loop
# The number of threads used on each run iterate from 1 to $MAXTHREADS
# After finishing the loop, the results will be dumped to ~/results.json

if [ -z $4 ]; then
    echo "Usage: $0 user@results-server user@mongod-server operation numthreads"
    exit 1
fi

RESULTS_SERVER=$1
MONGO_SERVER=$2
OPERATION=$3
MAXTHREADS=$4

source "$(dirname $0)/pbrc.sh"
bash "$(dirname $0)/startup.sh" $RESULTS_SERVER $MONGO_SERVER

# cd into the mongo repository
cd "$MONGO_DIR"

SERVER_INFO=$(ssh $MONGO_SERVER ~/mongo/perfbench/getserverinfo.sh)

for (( i=1; i<=$MAXTHREADS; i++ )); do
    ssh $MONGO_SERVER ~/mongo/perfbench/cleanandrestart.sh
    echo "Load testing with $i threads"
    configstr="globalExtraOption = {numThreads: $i, testServerInfo: $SERVER_INFO}"

    mongo --eval "$configstr" perfbench/$OPERATION.js
done

