#!/bin/bash

if [ -z "$1" ]; then
	echo "Must specify hosts file"
	exit 1
fi

HOSTS_FILE=$1

MONGOD_SERVER=$(head -n 1 $HOSTS_FILE)

tail -n +2 $HOSTS_FILE | while read host; do
	echo "$host -> $MONGOD_SERVER"
	ssh -n $host "~/mongo/perfbench/rampup.sh $MONGOD_SERVER"
	scp ${host}:results.json $host-results.json
	ssh -n $host "nohup ~/mongo/perfbench/holdit.sh $MONGOD_SERVER < /dev/null &> ~/holdit.log &" 
	scp ${host}:holdit.pid $host-holdit.pid
done

tail -n +2 $HOSTS_FILE | while read host; do
	if [ -f $host-holdit.pid ]; then
		echo "Killing holdit.sh on $host"
		ssh -n $host "kill $(cat $host-holdit.pid)" 
		rm $host-holdit.pid
	fi
done
