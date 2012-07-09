#!/usr/bin/env python

import sys
import os
import subprocess
from helpers import *
import json

def main():
    if len(sys.argv) < 4:
        return "Usage: " + sys.argv[0] + "results-server mongod-server operation numthreads"

    chdir('~/mongo')

    resurl = sys.argv[1] + '/experiment'
    dburl = sys.argv[2]
    operation = sys.argv[3]
    numthreads = int(sys.argv[4])

    options = {
        'numThreads': numthreads,
        'numSeconds': 10800,
        'saveResult': 'no',
        'databaseURL': dburl
    }

    configstr = 'globalExtraOption = %s' % json.dumps(options)

    writepid()

    print "Holding at %d threads" % numthreads

    while True:
        subprocess.call(['mongo', '--eval', configstr, 
            resurl, 'perfbench/%s.js' % operation])

if __name__ == '__main__':
    sys.exit(main())
