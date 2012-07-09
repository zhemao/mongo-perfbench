#!/usr/bin/env python

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
    threads = config['threads']

    p = sshpopen('python ~/mongo/perfbench/getserverinfo.py', stdout=subprocess.PIPE)
    (output, _) = p.communicate()
    config['server-info'] = json.loads(output)

    for host in config['load-servers']:
        s = json.dumps(config)

        p = sshpopen(host, "python ~/mongo/perfbench/rampup.py", stdin=subprocess.PIPE)
        p.communicate(s)
        
        command = "nohup python ~/mongo/perfbench/holdit.py %s %s %s %d \
                        < /dev/null &> ~/holdit.log &" % (resurl, dburl, operation, threads)
        sshcall(host, command)

        subprocess.call(["scp", "%s:holdit.pid" % host, "%s-holdit.pid" % host])

    for host in config['load-servers']:
        pidfilepath = '%s-holdit.pid' % host
        if os.path.isfile(pidfilepath):
            print "Killing holdit.py on %s" % host
            f = open(pidfilepath)
            pid = int(f.read().strip())
            f.close()
            sshcall(host, ['kill', pid, '&&', 'killall', 'mongo'])
            os.remove(pidfilepath)
