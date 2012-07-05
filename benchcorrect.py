#!/usr/bin/env python

import json
import sys

def main():
    numthreads = 0
    threadbase = 0

    for line in sys.stdin:
        data = json.loads(line.strip())
        
        oldnumthreads = numthreads
        numthreads = data['numThreads'] + threadbase

        if numthreads < oldnumthreads:
            threadbase = oldnumthreads
            numthreads = data['numThreads'] + threadbase
        
        data['numThreads'] = numthreads

        print json.dumps(data)

if __name__ == '__main__':
    main()
