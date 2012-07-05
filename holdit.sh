#!/bin/bash

# Runs the javascript benchmarks with 24 threads in an infinite loop
# The pid is written to ~/holdit.pid so that the script can be killed later

if [ -z $1 ]; then
    echo "Usage: $0 user@hostname"
    exit 1
fi

MONGO_SERVER=$1

source "$(dirname $0)/pbrc.sh"
bash "$(dirname $0)/startup.sh" $MONGO_SERVER

# cd into the mongo repository
cd "$MONGO_DIR"

SERVER_INFO='{hostname: "localhost:27018"}'

configstr="globalExtraOption = {numThreads: $MAXTHREADS, numSeconds: 7200, testServerInfo: $SERVER_INFO}"

echo -e $$ > ~/holdit.pid

echo "Holding at $MAXTHREADS threads"

while true; do
    mongo --eval "$configstr" perfbench/findone.js
done
