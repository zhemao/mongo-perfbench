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
    scriptname = 'perfbench/%s.js' % operation

    writepid()

    print "Holding at %d threads" % numthreads

    while True:
        subprocess.call(['mongo', '--eval', configstr, resurl, scriptname])

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
