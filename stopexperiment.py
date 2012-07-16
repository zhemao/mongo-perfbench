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

import os
import signal
import subprocess

# This script will stop a running experiment
# This script requires not arguments

def main():
    pidfilepath = '/tmp/perfbench.pid'

    if os.path.exists(pidfilepath):
        f = open(pidfilepath)
        pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            print "No such process"
        finally:
            f.close()
            os.remove(pidfilepath)

if __name__ == '__main__':
    main()
