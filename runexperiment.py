#    Copyright (C) 2012 10gen Inc.
#
#    This program is free software: you can redistribute it and/or  modify
#    it under the terms of the GNU Affero General Public License, version 3,
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Run a single experiment for a specific operation
# Usage: runexperiment.py operation suite config
#
# Operation is the operation that is to be run.
# It can be findone, insert, update, or inplace_insert.
# Suite is the name of the suite whose configuration will be pulled 
# from the result server.
# config is a json object that can be used to override the 
# "default config values" from the suite.

import sys
import os
import json
import subprocess
from helpers import *

def main():
    if len(sys.argv) < 4:
        print "Usage: " + sys.argv[0] + " operation suite config"
        return 1

    operation = sys.argv[1]
    suite = sys.argv[2]
    config = json.loads(sys.argv[3])

    chdir('~/mongo')

    # set up the string that will be passed in using --eval
    if suite == 'nosuite':
        configstr = 'globalExtraOption = %s;' % json.dumps(config)
    else:
        configstr = 'globalExtraOption = %s; suiteName = "%s";' % 
                        (json.dumps(config), suite)
    
    scriptname = 'perfbench/%s.js' % operation

    # start mongo
    proc = subprocess.Popen(['mongo', '--eval', configstr, 
                             '--nodb', scriptname])
    
    # write out the pid of the mongo process
    # this will allow stopexperiment.py to kill the process if necessary
    f = open('/tmp/perfbench.pid', 'w')
    f.write(str(proc.pid))
    f.close()

    # wait for the mongo process to stop and then exit with its returncode

    proc.wait()

    ret = proc.returncode

    if ret > 0:
        return ret

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
