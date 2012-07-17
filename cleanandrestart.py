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

# This script will stop mongod, restore the database to a clean state
# and then restart mongod.

import os
import platform
import signal
import subprocess
import sys
from helpers import fixpath

lockfilepath = os.path.expanduser('~/datadb/mongod.lock')

def kill_mongod(sig):
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
    if os.path.exists(lockfilepath) and os.path.getsize(lockfilepath) > 0:
        return kill_mongod(0)
    return False

def main():
    # kill the mongod process if it is running
    if dblocked():
        kill_mongod(signal.SIGINT)

    # wait for mongod to finish shutdown
    while dblocked():
        pass

    if platform.system() == 'Windows':
        dbsrc = 'D:\\basedb\\'
        dbdest = 'D:\\datadb'
    else:
        dbsrc = '/mnt/basedb/'
        dbdest = os.path.expanduser('~/datadb')

    # sync the database back to its original state
    subprocess.call(['rsync', '-avz', '--delete', dbsrc, dbdest])

    # restart mongod
    conffile = os.path.expanduser('~/.mongod.conf')
    return subprocess.call(['mongod', '-f', conffile, '--fork'])

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
