#!/usr/bin/env python

# Copyright 2012 10gen, Inc.

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


# This is the script that runs the show
# Usage: python runbench.py config.json
# See example.json for the configuration syntax
# Make sure whatever server this script is running from can ssh into
# the load servers and the database server without user input

import sys
import os
import subprocess
import time
from helpers import sshcall, sshpopen
import json
from optparse import OptionParser
import socket

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

def wait_for_connection(host, port):
    while True:
        try:
            conn = socket.create_connection((host, port))
            conn.close()
            break
        except socket.error:
            pass

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
        
        # wait until the server is ready to accept connections
        wait_for_connection(dbhost, 27017)

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
        rampup(host, noise_servers, prevhosts, config)

    # stop all the hold processes
    for host in load_servers:
        sshcall(host, 'python ~/mongo/perfbench/stopexperiment.py')

def main():
    parser = OptionParser(usage="%prog [options] configfile.json")
    parser.add_option('-o', '--operation', dest="operation", 
                      help="The operation to be run in this benchmark.")

    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.print_usage()
        return 1

    f = open(args[0])

    try: 
        config = json.load(f)
    except ValueError:
        print "Could not load JSON"
        return 1
    finally:
        f.close()

    if options.operation:
        if options.operation == 'all':
            operations = ['findone', 'insert', 'update', 'inplace_update']
        else:
            operations = [options.operation]
        
        for op in operations:
            config['operation'] = op
            run_benchmark(config)
    else:
        run_benchmark(config)

if __name__ == '__main__':
    sys.exit(main())
