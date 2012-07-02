#!/bin/bash

KNAME=$(uname -s)
KVER=$(uname -v)
KREL=$(uname -r)
ARCH=$(uname -p)

if [ $KNAME == 'Linux' ]; then
	OS=$(uname -o)
	FS=$(df -T ~/datadb | awk 'NR == 2 {print $2}')
elif [ $KNAME == 'Darwin' ]; then
	# These are all pretty much assumptions. 
	# Mac OSX doesn't really provide utilities to query for this info
	OS='Mac OSX'
	FS='HFS+' 
fi

echo "{hostname: \"localhost:27018\", kernelName: \"$KNAME\", \
		kernelVersion: \"$KVER\", kernelRelease: \"$KREL\", \
		Platform: \"$ARCH\", fileSystem: \"$FS\", OS: \"$OS\"}"
		
