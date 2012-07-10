import os
import signal
import subprocess
import glob
import sys
from helpers import fixpath

lockfilepath = os.path.expanduser('~/datadb/mongod.lock')

def dblocked():
    return os.path.exists(lockfilepath) and os.path.getsize(lockfilepath) > 0

def main():
    if dblocked():
        f = open(lockfilepath)
        pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        f.close()

    while dblocked():
        pass

    dbfiles = glob.glob('/mnt/basedb/*')
    dbloc = os.path.expanduser('~/datadb')

    subprocess.call(['rsync', '-avz', '--delete'] + dbfiles + [dbloc])

    conffile = os.path.expanduser('~/.mongod.conf')
    return subprocess.call(['mongod', '-f', conffile, '--fork'])

if __name__ == '__main__':
    fixpath()
    sys.exit(main())
