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
        opsys = ' '.join(platform.dist())
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
