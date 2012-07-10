import os
import signal
import subprocess

def main():
    pidfilepath = os.path.expanduser('~/holdit.pid')

    if os.path.exists(pidfilepath):
        f = open(pidfilepath)
        pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            print "No such process"
        f.close()
        subprocess.call(['killall', 'mongo'])
        os.remove(pidfilepath)

if __name__ == '__main__':
    main()
