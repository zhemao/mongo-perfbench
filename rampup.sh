#!/bin/bash

# This script runs the javascript benchmarks in a loop
# The number of threads used on each run iterate from 1 to $MAXTHREADS
# After finishing the loop, the results will be dumped to ~/results.json

if [ -z $3 ]; then
    echo "Usage: $0 user@hostname operation numthreads"
    exit 1
fi

MONGO_SERVER=$1
OPERATION=$2
MAXTHREADS=$3

bash "$(dirname $0)/cleanandrestart.sh"

source "$(dirname $0)/pbrc.sh"
bash "$(dirname $0)/startup.sh" $MONGO_SERVER

# cd into the mongo repository
cd "$MONGO_DIR"

SERVER_INFO=$(ssh $MONGO_SERVER ~/mongo/perfbench/getserverinfo.sh)

for (( i=1; i<=$MAXTHREADS; i++ )); do
    ssh $MONGO_SERVER ~/mongo/perfbench/cleanandrestart.sh
    echo "Load testing with $i threads"
    configstr="globalExtraOption = {numThreads: $i, testServerInfo: $SERVER_INFO}"

    mongo --eval "$configstr" perfbench/$OPERATION.js
done

mongoexport -d experiment -c results -o ~/results.json
