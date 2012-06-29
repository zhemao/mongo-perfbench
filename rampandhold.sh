#!/bin/bash

# Runs the benchmark scripts with 1 to 24 threads and then holds on 24
# First argument is the server where mongod is located

PERFBENCH_DIR="$(dirname $0)"
MONGO_DIR="$(dirname $PERFBENCH_DIR)"

source "$PERFBENCH_DIR/shellrc.sh"

if [ -z $1 ]; then
    echo "Usage: $0 user@hostname"
    exit 1
fi

MONGO_SERVER=$1
SERVER_INFO='{hostname: "localhost:27018"}'

# cd into the mongo repository
cd "$MONGO_DIR"

# start mongod if necessary
if ! lsof -i :27017 > /dev/null; then
    mongod -f ~/.mongod.conf --fork
fi

# start ssh tunnel if necessary
if ! lsof -i :27018 > /dev/null; then
    ssh -fN -L 27018:localhost:27017 $MONGO_SERVER
fi

for i in {1..24}; do
    ssh $MONGO_SERVER ~/mongo/perfbench/cleanandrestart.sh
    configstr="globalExtraOption = {numThreads: $i, testServerInfo: $SERVER_INFO}"
    for operation in insert update findone; do
        mongo localhost:27018 --eval "$configstr" perfbench/$operation.js
    done
done

