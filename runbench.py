#!/usr/bin/env python

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

def start_noise(host, baseconfig):
    """Start a noise operation on host
       The baseconfig argument is the config read from the json file."""

    config = dict(baseconfig)
    config['operation'] = 'findone'

    return start_hold(host, config)

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
        'numSeconds': baseconfig.get('seconds', 120),
        'numTrials': baseconfig.get('trials', 5)
    }

    configstr = "'" + json.dumps(config) + "'"

    command = ['python', '~/mongo/perfbench/runexperiment.py', 
               operation, suite, configstr]

    return sshcall(host, command)

def rampup(host, noisehosts, prevhosts, config):
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

        # Restart the noise servers
        for nhost in noisehosts:
            print "Restarting noise on %s" % nhost
            sshcall(nhost,'python ~/mongo/perfbench/stopexperiment.py')
            start_noise(nhost, config)

        # Restart all the hold operations
        for phost in prevhosts:
            print "Restarting hold on %s" % phost
            sshcall(phost, 'python ~/mongo/perfbench/stopexperiment.py')
            start_hold(phost, config)

        # sleep for a few seconds to wait for the other 
        # load servers to warm up
        time.sleep(2)

        # calculate the number of threads running on the other servers 
        extern = len(prevhosts) * maxthreads

        print "Load testing with %d threads and %d external" % (i, extern)

        run_experiment(host, i, extern, config)

def run_benchmark(config):
    """Run the entire benchmark using the given configuration"""
    dburl = config['database-server']
    load_servers = config['load-servers']
    noise_servers = config.get('noise-servers', [])

    # get information from the test database server
    p = sshpopen(dburl, 'python ~/mongo/perfbench/getserverinfo.py', 
                 stdout=subprocess.PIPE)
    (output, _) = p.communicate()
    config['server-info'] = json.loads(output)
    
    # clean up any processes left over from previous scripts
    for host in load_servers:
        sshcall(host, 'python ~/mongo/perfbench/stopexperiment.py')

    # run the benchmark
    for (i, host) in enumerate(load_servers):
        prevhosts = load_servers[:i]
        rampup(host, noisehosts, prevhosts, config)

    # stop all the hold processes
    for host in load_servers:
        sshcall(host, 'python ~/mongo/perfbench/stopexperiment.py')

def main():
    if len(sys.argv) < 2:
        print "Usage: " + sys.argv[0] + ' configfile.json'
        return 1

    f = open(sys.argv[1])
    config = json.load(f)
    f.close()

    run_benchmark(config)

if __name__ == '__main__':
    sys.exit(main())
