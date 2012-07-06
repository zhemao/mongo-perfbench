#!/bin/bash

# Runs the javascript benchmarks with $NUMTHREADS threads in an infinite loop
# The pid is written to ~/holdit.pid so that the script can be killed later

if [ -z $3 ]; then
    echo "Usage: $0 user@results-server user@mongod-server operation numthreads"
    exit 1
fi

RESULTS_SERVER=$1
MONGO_SERVER=$2
OPERATION=$3
NUMTHREADS=$4

source "$(dirname $0)/pbrc.sh"

# cd into the mongo repository
cd "$MONGO_DIR"

configstr="globalExtraOption = {numThreads: $NUMTHREADS, numSeconds: 7200, databaseURL: \"$MONGO_SERVER\"}"

echo -e $$ > ~/holdit.pid

echo "Holding at $NUMTHREADS threads"

while true; do
    mongo --eval "$configstr" $RESULTS_SERVER perfbench/$OPERATION.js
done
