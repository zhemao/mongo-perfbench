# Copyright 2012 10gen, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Various helper functions used by the other scripts

import os
import sys
import subprocess

def chdir(path='~'):
    """change the current directory, expanding any user aliases in path"""
    os.chdir(os.path.expanduser(path))

def sshpopen(host, command, **kwargs):
    """run a command on a remote host using subprocess.Popen"""
    if isinstance(command, list):
        command = ' '.join(command)
    return subprocess.Popen(['ssh', '-n', host, command], **kwargs)

def sshcall(host, command, **kwargs):
    """run a command on a remote host using subprocess.call"""
    if isinstance(command, list):
        command = ' '.join(command)
    return subprocess.call(['ssh', '-n', host, command], **kwargs)

def fixpath():
    """fix the PATH variable in the current environment such that the bin
    directory in the user's home directory is included"""
    homebin = os.path.expanduser('~/bin')
    if not os.path.isdir(homebin):
        return
    if homebin not in os.getenv('PATH').split(os.pathsep):
        os.environ['PATH'] = homebin + os.pathsep + os.getenv('PATH')
