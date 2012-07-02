#!/bin/bash

# Shuts down the database, deletes the files, and restarts

source "$(dirname $0)/pbrc.sh"

if lsof -i :27017 > /dev/null; then
    killall mongod
fi

rm -rf ~/datadb
mkdir ~/datadb

mongod -f ~/.mongod.conf --fork
