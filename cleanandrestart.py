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

# This script will stop mongod, restore the database to a clean state
# and then restart mongod.

import os
import platform
import pymongo
from pymongo.errors import AutoReconnect
import signal
import subprocess
import sys
from helpers import fixpath

if platform.system() == 'Windows':
    lockfilepath = 'D:\\datadb\\mongod.lock'
else:
    lockfilepath = '/mnt/datadb/mongod.lock'

def send_signal(sig):
    """Send the signal sig to the running mongod process.
       Returns True if the signal was sent successfully.
       Return False if no mongod process is running."""
    # read in the pid from the lockfile
    f = open(lockfilepath)
    pid = f.read().strip()
    f.close()

    if len(pid) == 0:
        return False
    
    try:
        # send the signal to the process with that pid
        os.kill(int(pid), sig)
        return True
    except OSError:
        return False

def dblocked():
    """Determine whether a mongod process is running"""
    if platform.system() == 'Windows':
        proc = subprocess.Popen(['tasklist', '/FI', 'IMAGENAME eq mongod.exe'], 
                                stdout=subprocess.PIPE)
        (out, err) = proc.communicate()

        return not out.startswith('INFO: No tasks are running')
    else:
        if os.path.exists(lockfilepath) and os.path.getsize(lockfilepath) > 0:
            return send_signal(0)
        return False

def kill_mongod():
    try:
        conn = pymongo.Connection()
        conn.admin.command('shutdown')
    except AutoReconnect:
        pass

def start_mongod():
    conffile = os.path.expanduser('~/.mongod.conf')
    if platform.system() == 'Windows':
        os.spawnl(os.P_NOWAIT, 'mongod', 'mongod', '-f', conffile)
        return 0
    else:
        return subprocess.call(['mongod', '-f', conffile, '--fork'])

def main():
    # kill the mongod process if it is running
    if dblocked():
        kill_mongod()

    # wait for mongod to finish shutdown
    while dblocked():
        pass

    if platform.system() == 'Windows':
        dbsrc = '/cygdrive/d/basedb/'
        dbdest = '/cygdrive/d/datadb'
    else:
        dbsrc = '/mnt/basedb/'
        dbdest = '/mnt/datadb'

    # sync the database back to its original state
    subprocess.call(['rsync', '-avz', '--delete', dbsrc, dbdest])

    # restart mongod
    return start_mongod()

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
