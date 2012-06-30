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

configstr="globalExtraOption = {numThreads: 24, testServerInfo: $SERVER_INFO}"

while true; do
    mongo localhost:27018 --eval "$configstr" perfbench/findone.js
done
