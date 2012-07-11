import sys
import os
import json
import subprocess
from helpers import *

# Run a single experiment.
# Usage: runexperiment.py operation suite config
# Operation is the operation that is to be run.
# It can be findone, insert, update, or inplace_insert.
# Suite is the name of the suite whose configuration will be pulled 
# from the result server.
# Config is a json object that will be passed in as the globalExtraOption
# variable to the javascript code.

def main():
    if len(sys.argv) < 4:
        return "Usage: " + sys.argv[0] + " operation suite config"

    operation = sys.argv[1]
    suite = sys.argv[2]
    config = json.loads(sys.argv[3])

    chdir('~/mongo')

    if suite == 'nosuite':
        configstr = 'globalExtraOption = %s;' % json.dumps(config)
    else:
        configstr = 'globalExtraOption = %s; suiteName = "%s";' % (json.dumps(config), suite)
    
    scriptname = 'perfbench/%s.js' % operation

    proc = subprocess.Popen(['mongo', '--eval', configstr, '--nodb', scriptname])
    
    f = open('/tmp/perfbench.pid', 'w')
    f.write(str(proc.pid))
    f.close()

    proc.wait()

    ret = proc.returncode

    if ret > 0:
        return ret

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
