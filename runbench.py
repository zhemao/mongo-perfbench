#!/usr/bin/env python

# This is the script that starts it all
# Usage: python runbench.py config.json
# See example.json for the configuration syntax

import sys
import os
import subprocess
from helpers import *
import json

def main():
    if len(sys.argv) < 2:
        return "Usage: " + sys.argv[0] + ' configfile.json'

    f = open(sys.argv[1])
    config = json.load(f)
    f.close()

    resurl = config['results-server']
    dburl = config['database-server']
    operation = config['operation']
    threads = config['maxthreads']

    p = sshpopen(dburl, 'python ~/mongo/perfbench/getserverinfo.py', stdout=subprocess.PIPE)
    (output, _) = p.communicate()
    config['server-info'] = json.loads(output)

    config['extern-threads'] = 0

    for host in config['load-servers']:
        print host + "->" + dburl

        configstr = "'" + json.dumps(config) + "'"

        ret = sshcall(host, ['python', '~/mongo/perfbench/rampup.py', configstr])

        if ret != 0:
            print "rampup returned abnormally - aborting..."
            break
        
        command = "nohup python ~/mongo/perfbench/holdit.py %s %s %d \
                        < /dev/null &> ~/holdit.log &" % (dburl, operation, threads)
        sshcall(host, command)
        
        config['extern-threads'] += config['maxthreads']

    for host in config['load-servers']:
        sshcall(host, 'python ~/mongo/perfbench/stophold.py')

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
