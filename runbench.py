#!/usr/bin/env python

# This is the script that runs the show
# Usage: python runbench.py config.json
# See example.json for the configuration syntax
# Make sure whatever server this script is running from can ssh into
# the load servers and the database server without user input

import sys
import os
import subprocess
import time
from helpers import *
import json

def start_hold(host, baseconfig):
    """Start a hold operation on host.
       The baseconfig argument is the config read from the json file."""
    
    operation = baseconfig['operation']
    suite = baseconfig.get('suite', 'nosuite')

    config = {
        'numTrials': 1,
        'numSeconds': 10800,
        'databaseURL': baseconfig['database-server'],
        'saveResult': 'no'
    }

    configstr = "'" + json.dumps(config) + "'"

    command = ['nohup', 'python', '~/mongo/perfbench/runexperiment.py', 
               operation, suite, configstr,
               '<', '/dev/null', '&>', '~/holdit.log', '&']
    
    return sshcall(host, command)

def run_experiment(host, threads, extern, baseconfig):
    """Start an experiment on host using the given number of threads 
       and external threads. Baseconfig is the config read from the
       json file."""

    operation = baseconfig['operation']
    suite = baseconfig.get('suite', 'nosuite')
    
    config = {
        'numThreads': threads,
        'externThreads': extern,
        'databaseURL': baseconfig['database-server'],
        'resultURL': baseconfig['results-server'],
        'testServerInfo': baseconfig['server-info'],
        'numSeconds': baseconfig['seconds']
    }

    configstr = "'" + json.dumps(config) + "'"

    command = ['python', '~/mongo/perfbench/runexperiment.py', 
               operation, suite, configstr]

    return sshcall(host, command)

def rampup(host, prevhosts, config):
    """Run a series of experiments on host, starting with increment and going
       up by increment until maxthreads is reached. Hold operations will
       be run on the hosts in prevhosts. Config is the configuration
       read from the json file."""

    maxthreads = config['maxthreads']
    incr = config['increment']
    dbhost = config['database-server']

    for i in range(incr, maxthreads+1, incr):
        print "Restarting database"
        sshcall(dbhost, 'python ~/mongo/perfbench/cleanandrestart.py')

        # Restart all the hold operations
        for phost in prevhosts:
            print "Restarting hold on %s" % phost
            sshcall(phost, 'python ~/mongo/perfbench/stopexperiment.py')
            start_hold(phost, config)

        time.sleep(2)

        extern = len(prevhosts) * maxthreads

        print "Load testing with %d threads and %d external" % (i, extern)

        run_experiment(host, i, extern, config)

def run_benchmark(config):
    dburl = config['database-server']
    load_servers = config['load-servers']

    p = sshpopen(dburl, 'python ~/mongo/perfbench/getserverinfo.py', stdout=subprocess.PIPE)
    (output, _) = p.communicate()
    config['server-info'] = json.loads(output)

    for (i, host) in enumerate(load_servers):
        prevhosts = load_servers[:i]
        rampup(host, prevhosts, config)

    for host in load_servers:
        sshcall(host, 'python ~/mongo/perfbench/stopexperiment.py')

def main():
    if len(sys.argv) < 2:
        return "Usage: " + sys.argv[0] + ' configfile.json'

    f = open(sys.argv[1])
    config = json.load(f)
    f.close()

    run_benchmark(config)

if __name__ == '__main__':
    sys.exit(main())
