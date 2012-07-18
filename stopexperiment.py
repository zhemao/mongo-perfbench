#!/usr/bin/env python

# Copyright 2012 10gen, Inc.
#
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
