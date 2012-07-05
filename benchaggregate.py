#!/usr/bin/env python

import json
import sys

def main():
    if len(sys.argv) == 1:
        print "Usage: %s file1.json [file2.json ...]" % sys.argv[0]
        sys.exit(1)

    numthreads = 0
    threadbase = 0

    for fname in sys.argv[1:]:
        f = open(fname)
        for line in f:
            data = json.loads(line.strip())
            
            oldnumthreads = numthreads
            numthreads = data['numThreads'] + threadbase

            if numthreads < oldnumthreads:
                threadbase = oldnumthreads
                numthreads = data['numThreads'] + threadbase
            
            data['numThreads'] = numthreads

            print json.dumps(data)
        f.close()

if __name__ == '__main__':
    main()
