import os
import signal
import subprocess
import sys
from helpers import fixpath

# Stop mongod if running
# Restore the database to a previous state using rsync
# Restart mongod

lockfilepath = os.path.expanduser('~/datadb/mongod.lock')

def kill_mongod(sig):
    try:
        f = open(lockfilepath)
        pid = f.read().strip()
        if len(pid) == 0:
            return 1
        os.kill(int(pid), sig)
        f.close()
        return 0
    except OSError:
        return 1

def dblocked():
    if os.path.exists(lockfilepath) and os.path.getsize(lockfilepath) > 0:
        return not kill_mongod(0)
    return False

def main():
    if dblocked():
        kill_mongod(signal.SIGINT)

    while dblocked():
        pass

    dbsrc = '/mnt/basedb/'
    dbdest = os.path.expanduser('~/datadb')

    subprocess.call(['rsync', '-avz', '--delete', dbsrc, dbdest])

    conffile = os.path.expanduser('~/.mongod.conf')
    return subprocess.call(['mongod', '-f', conffile, '--fork'])

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
