#!/bin/bash

# Shuts down the database, deletes the files, and restarts

source "$(dirname $0)/pbrc.sh"

if lsof -i :27017 > /dev/null; then
    killall mongod
fi

#rm -rf ~/datadb
#cp -r ~/basedb ~/datadb

rsync -avz --delete ~/basedb/* ~/datadb

mongod -f ~/.mongod.conf --fork
