#!/bin/bash

# This script runs the javascript benchmarks in a loop
# The number of threads used on each run iterate from 1 to 24
# After finishing the loop, the results will be dumped to ~/results.json

if [ -z $1 ]; then
    echo "Usage: $0 user@hostname"
    exit 1
fi

MONGO_SERVER=$1

bash "$(dirname $0)/cleanandrestart.sh"

source "$(dirname $0)/pbrc.sh"
bash "$(dirname $0)/startup.sh" $MONGO_SERVER

# cd into the mongo repository
cd "$MONGO_DIR"

SERVER_INFO=$(ssh $MONGO_SERVER ~/mongo/perfbench/getserverinfo.sh)

for i in {1..24}; do
    ssh $MONGO_SERVER ~/mongo/perfbench/cleanandrestart.sh
    echo "Load testing with $i threads"
    configstr="globalExtraOption = {numThreads: $i, testServerInfo: $SERVER_INFO}"
    for operation in insert update findone; do
        mongo --eval "$configstr" perfbench/$operation.js
    done
done

mongoexport -d experiment -c results -o ~/results.json
