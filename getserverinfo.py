#!/usr/bin/env python

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
