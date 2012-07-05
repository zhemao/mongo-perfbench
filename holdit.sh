#!/bin/bash

# Runs the javascript benchmarks with $NUMTHREADS threads in an infinite loop
# The pid is written to ~/holdit.pid so that the script can be killed later

if [ -z $3 ]; then
    echo "Usage: $0 user@hostname operation numthreads"
    exit 1
fi

MONGO_SERVER=$1
OPERATION=$2
NUMTHREADS=$3

source "$(dirname $0)/pbrc.sh"
bash "$(dirname $0)/startup.sh" $MONGO_SERVER

# cd into the mongo repository
cd "$MONGO_DIR"

SERVER_INFO='{hostname: "localhost:27018"}'

configstr="globalExtraOption = {numThreads: $NUMTHREADS, numSeconds: 7200, testServerInfo: $SERVER_INFO}"

echo -e $$ > ~/holdit.pid

echo "Holding at $NUMTHREADS threads"

while true; do
    mongo --eval "$configstr" perfbench/$OPERATION.js
done
