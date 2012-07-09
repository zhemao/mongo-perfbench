import os
import signal
import subprocess
import glob

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

    command = os.path.expanduser('mongod -f ~/.mongod.conf --fork')
    return subprocess.call(command)

if __name__ == '__main__':
    sys.exit(main())
