import os
import signal
import subprocess
import sys
from helpers import fixpath

# This script will stop mongod, restore the database to a previous state
# and then restart mongod.

lockfilepath = os.path.expanduser('~/datadb/mongod.lock')

def kill_mongod(sig):
    """Send the signal sig to the running mongod process"""
    try:
        # read in the pid from the lockfile
        f = open(lockfilepath)
        pid = f.read().strip()
        if len(pid) == 0:
            return 1
        # send the signal to the process with that pid
        os.kill(int(pid), sig)
        f.close()
        return 0
    except OSError:
        return 1

def dblocked():
    """Determine whether a mongod process is running"""
    if os.path.exists(lockfilepath) and os.path.getsize(lockfilepath) > 0:
        return not kill_mongod(0)
    return False

def main():
    # kill the mongod process if it is running
    if dblocked():
        kill_mongod(signal.SIGINT)

    # wait for mongod to finish shutdown
    while dblocked():
        pass

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
