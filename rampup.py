import sys
import os
import json
import subprocess
from helpers import *

def main():
    if len(sys.argv) < 2:
        return "Usage: " + sys.argv[0] + " config"

    config = json.loads(sys.argv[1])

    chdir('~/mongo')

    incr = config['increment']
    maxthreads = config['threads']
    suite = config['suite']
    operation = config['operation']
    dburl = config['database-server']
    resurl = config['results-server'] + '/experiment'

    for i in range(incr, maxthreads+1, incr):
        sshcall(dburl, 'python ~/mongo/perfbench/cleanandrestart.py')
        print "Load testing with %d threads" % i
        options = {
            "numThreads": i,
            "databaseURL": dburl,
            "testServerInfo": config['server-info']
        }

        configstr = 'globalExtraOption = %s; suiteName = "%s";' % (json.dumps(options), suite)

        scriptname = 'perfbench/%s.js' % operation

        ret = subprocess.call(['mongo', '--eval', configstr, resurl, 'perfbench/%s.js'])

        if ret > 0:
            return ret

if __name__ == '__main__':
    sys.exit(main())
