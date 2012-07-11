#!/usr/bin/env python

# Runs the benchmarks continuously using a fixed number of threads
# Usage: python holdit.py results-server mongod-server operation numtreads

import sys
import os
import subprocess
from helpers import *
import json

def main():
    if len(sys.argv) < 4:
        return "Usage: " + sys.argv[0] + "mongod-server operation numthreads"

    chdir('~/mongo')

    dburl = sys.argv[1]
    operation = sys.argv[2]
    numthreads = int(sys.argv[3])

    options = {
        'numThreads': numthreads,
        'numSeconds': 10800,
        'saveResult': 'no',
        'databaseURL': dburl
    }

    configstr = 'globalExtraOption = %s' % json.dumps(options)
    scriptname = 'perfbench/%s.js' % operation

    writepid()

    print "Holding at %d threads" % numthreads

    while True:
        print "Starting load"
        subprocess.call(['mongo', '--eval', configstr, '--nodb', scriptname])

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
