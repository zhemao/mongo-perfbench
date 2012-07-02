#!/bin/bash

# Runs the benchmark scripts with 1 to 24 threads and then holds on 24
# First argument is the server where mongod is located

if [ -z $1 ]; then
    echo "Usage: $0 user@hostname"
    exit 1
fi

MONGO_SERVER=$1

bash "$(dirname $0)/cleanandrestart.sh"

source "$(dirname $0)/pbrc.sh"
bash "$(dirname $0)/startup.sh" $MONGO_SERVER

echo "Ramping up..."
bash "$(dirname $0)/rampup.sh" $MONGO_SERVER

echo "Dumping data"
mongoexport -d experiment -c results -o ~/testinfo.json

echo "Holding..."
nohup bash "$(dirname $0)/holdit.sh" $MONGO_SERVER &

echo -e $! > ~/holdit.pid

exit
