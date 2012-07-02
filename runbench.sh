#!/bin/bash

if [ -z "$1" ]; then
	echo "Must specify hosts file"
	exit 1
fi

HOSTS_FILE=$1

MONGOD_SERVER=$(head -n 1 $HOSTS_FILE)

tail -n +2 $HOSTS_FILE | while read host; do
	ssh $host "~/mongo/perfbench/rampandhold.sh $MONGOD_SERVER"
	scp ${host}:testinfo.json $host-testinfo.json
	scp ${host}:holdit.pid $host-holdit.pid
done

tail -n +2 $HOSTS_FILE | while read host; do
	ssh $host "kill $(cat $host-holdit.pid)" 
done
