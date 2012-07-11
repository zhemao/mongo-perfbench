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
    if len(sys.argv) < 4:
        return "Usage: " + sys.argv[0] + " operation suite config"

    operation = sys.argv[1]
    suite = sys.argv[2]
    config = json.loads(sys.argv[3])

    chdir('~/mongo')

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
