import sys
import os
import json
import subprocess
from helpers import *

# Run the benchmarks continuously, ramping up the number of threads each time
# Usage: python rampup.py config
# config is a json string
# see example.json for the configuration syntax

def main():
    if len(sys.argv) < 2:
        return "Usage: " + sys.argv[0] + " config"

    config = json.loads(sys.argv[1])

    chdir('~/mongo')

    incr = config['increment']
    maxthreads = config['maxthreads']
    suite = config['suite']
    operation = config['operation']
    dburl = config['database-server']
    resurl = config['results-server'] 

    for i in range(incr, maxthreads+1, incr):
        sshcall(dburl, 'python ~/mongo/perfbench/cleanandrestart.py')
        print "Load testing with %d - %d threads" % (config['extern-threads'], i)
        options = {
            "numThreads"    : i,
            "databaseURL"   : dburl,
            "resultURL"    : resurl,
            "testServerInfo": config['server-info'],
            "externThreads" : config['extern-threads'],
            "numSeconds"    : config['seconds']
        }

        configstr = 'globalExtraOption = %s; suiteName = "%s";' % (json.dumps(options), suite)

        scriptname = 'perfbench/%s.js' % operation

        ret = subprocess.call(['mongo', '--eval', configstr, '--nodb', scriptname])

        if ret > 0:
            return ret

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
