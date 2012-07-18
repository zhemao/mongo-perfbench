# Copyright 2012 10gen, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    if len(sys.argv) < 3:
        print "Usage: " + sys.argv[0] + " operation suite [config]"
        return 1

    operation = sys.argv[1]
    suite = sys.argv[2]

    if len(sys.argv) < 4:
        config = {}
    else:
        config = json.loads(sys.argv[3])

    chdir('~/mongo')

    # set up the string that will be passed in using --eval
    if suite == 'nosuite':
        configstr = 'globalExtraOption = %s;' % json.dumps(config)
    else:
        configstr = ('globalExtraOption = %s; '
                     'suiteName = "%s";') % (json.dumps(config), suite)
    
    scriptname = 'perfbench/%s.js' % operation

    # start mongo
    proc = subprocess.Popen(['mongo', '--eval', configstr, 
                             '--nodb', scriptname])
    
    # write out the pid of the mongo process
    # this will allow stopexperiment.py to kill the process if necessary
    f = open('/tmp/perfbench.pid', 'w')
    try:
        f.write(str(proc.pid))
    finally:
        f.close()

    # wait for the mongo process to stop and then exit with its returncode

    proc.wait()

    ret = proc.returncode

    if ret > 0:
        return ret

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
