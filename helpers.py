import os
import sys
import subprocess

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

# Various helper functions used by the other scripts

# change the current directory
# user aliases will be expanded
def chdir(path='~'):
    os.chdir(os.path.expanduser(path))

# run a command on a remote host using subprocess.Popen
def sshpopen(host, command, **kwargs):
    if isinstance(command, list):
        command = ' '.join(command)
    return subprocess.Popen(['ssh', '-n', host, command], **kwargs)

# run a command on a remote host using subprocess.call
def sshcall(host, command, **kwargs):
    if isinstance(command, list):
        command = ' '.join(command)
    return subprocess.call(['ssh', '-n', host, command], **kwargs)

def fixpath():
    homebin = os.path.join(os.getenv('HOME'), 'bin')
    if homebin not in os.getenv('PATH').split(os.pathsep):
        os.environ['PATH'] = homebin + os.pathsep + os.getenv('PATH')
