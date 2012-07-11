import os
import signal
import subprocess

def main():
    pidfilepath = '/tmp/perfbench.pid'

    if os.path.exists(pidfilepath):
        f = open(pidfilepath)
        pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            print "No such process"
        f.close()
        os.remove(pidfilepath)

if __name__ == '__main__':
    main()
