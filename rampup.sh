#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: $0 user@hostname"
    exit 1
fi

MONGO_SERVER=$1

source "$(dirname $0)/pbrc.sh"
bash "$(dirname $0)/startup.sh" $MONGO_SERVER

# cd into the mongo repository
cd "$MONGO_DIR"

for i in {1..24}; do
    ssh $MONGO_SERVER ~/mongo/perfbench/cleanandrestart.sh
    echo "Load testing with $i threads"
    configstr="globalExtraOption = {numThreads: $i, testServerInfo: $SERVER_INFO}"
    for operation in insert update findone; do
        mongo localhost:27018 --eval "$configstr" perfbench/$operation.js
    done
done

