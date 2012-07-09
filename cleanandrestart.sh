#!/bin/bash

# Shuts down the database, deletes the files, and restarts

source "$(dirname $0)/pbrc.sh"

if lsof -i :27017 > /dev/null; then
    killall mongod
fi

#rm -rf ~/datadb
#cp -r ~/basedb ~/datadb

# wait until lock is released
while [ -f ~/datadb/mongod.lock ] && kill -0 $(cat ~/datadb/mongod.lock); do
    sleep 1
done

rsync -avz --delete /mnt/basedb/* ~/datadb

mongod -f ~/.mongod.conf --fork
