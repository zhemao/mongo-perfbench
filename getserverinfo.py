#!/usr/bin/env python

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

# Creates a sysinfo document. The script runs the 'uname' command on the OS,
# parses the output from that command and plugs it into the sysinfo document.
# There are some assumptions/caveats here :
# Assumption 1 : If the OS is Windows then the filesystem is assumed to be NTFS.
# Assumption 2 : If the OS is Darwin then the OS/filesystem is assumed to be Mac/HFS+.


import platform
import os
import subprocess
import json

def main():
    kname, hostname, krel, kver, arch, _ = platform.uname()
    datadir = os.path.expanduser('~/datadb')
    
    if kname == 'Linux':
        p = subprocess.Popen(['df', '-T', datadir], stdout=subprocess.PIPE)
        (output, _) = p.communicate()
        fs = [s for s in output.split('\n')[1].split(' ') if len(s) > 0][1]
        opsys = ' '.join(platform.linux_distribution())
    elif kname == 'Darwin':
        fs = 'HFS+'
        opsys = 'Mac OSX ' + platform.mac_ver()[0]
    elif kname == 'Windows':
        fs = 'NTFS'
        opsys = kname + ' ' + krel

    sysinfo = {
        'hostname': hostname,
        'kernelName': kname,
        'kernelVersion': kver,
        'kernelRelease': krel,
        'Platform': arch,
        'fileSystem': fs,
        'OS': opsys
    }

    print json.dumps(sysinfo)

if __name__ == '__main__':
    main()
