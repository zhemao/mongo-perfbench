import os
import sys
import subprocess

def chdir(path='~'):
    os.chdir(os.path.expanduser(path))

def sshpopen(host, command, **kwargs):
    if isinstance(command, list):
        command = ' '.join(command)
    command = os.path.expanduser(command)
    return subprocess.Popen(['ssh', '-n', host, command], **kwargs)

def sshcall(host, command, **kwargs):
    if isinstance(command, list):
        command = ' '.join(command)
    command = os.path.expanduser(command)
    return subprocess.call(['ssh', '-n', host, command], **kwargs)

def writepid():
    pid = os.getpid()
    bname = os.path.basename(sys.argv[0])
    name, ext = os.path.splitext(bname)

    pidfilepath = os.path.join(os.getenv('HOME'), name + '.pid')

    f = open(pidfilepath, 'w')
    f.write(str(pid))
    f.close()

def fixpath():
    homebin = os.path.join(os.getenv('HOME'), 'bin')
    if homebin not in os.getenv('PATH').split(os.pathsep):
        os.environ['PATH'] = os.pathsep.join(homebin, os.getenv('PATH'), '/sbin', '/usr/sbin')
