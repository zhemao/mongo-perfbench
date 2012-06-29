#!/bin/bash

if lsof -i :27017 > /dev/null; then
    killall mongod
fi

rm -rf ~/datadb
cp -r ~/basedb ~/datadb

mongod -f ~/.mongod.conf --fork
