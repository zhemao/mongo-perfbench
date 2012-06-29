#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: $0 user@hostanme"
    exit 1
fi

MONGO_SERVER=$1

# start mongod if necessary
if ! lsof -i :27017 > /dev/null; then
    mongod -f ~/.mongod.conf --fork
fi

# start ssh tunnel if necessary
if ! lsof -i :27018 > /dev/null; then
    ssh -fN -L 27018:localhost:27017 $MONGO_SERVER
fi
