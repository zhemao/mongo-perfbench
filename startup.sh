#!/bin/bash

# Starts mongod and the ssh tunnel if necessary

if [ -z $2 ]; then
    echo "Usage: $0 user@results-server user@mongod-server"
    exit 1
fi

RESULTS_SERVER=$1
MONGO_SERVER=$2

# start ssh tunnels if necessary
if ! /usr/sbin/lsof -i :27017 > /dev/null; then
    ssh -fN -L 27017:localhost:27017 $RESULTS_SERVER
fi

if ! /usr/sbin/lsof -i :27018 > /dev/null; then
    ssh -fN -L 27018:localhost:27017 $MONGO_SERVER
fi
