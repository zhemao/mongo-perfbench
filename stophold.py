import os
import signal
import subprocess

def main():
    pidfilepath = os.path.expanduser('~/holdit.pid')

    if os.path.exists(pidfilepath):
        f = open(pidfilepath)
        pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        f.close()
        subprocess.call('killall mongo')
