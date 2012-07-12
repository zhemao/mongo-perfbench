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

# Runs a set of benchmarks using the given configuration
# The operation field is ignored
# Instead this script will iterate through all possible operations

from runbench import run_benchmark
import json
import sys

def main():
    if len(sys.argv) < 2:
        print "Usage: " + sys.argv[0] + ' configfile.json'
        return 1

    f = open(sys.argv[1])
    config = json.load(f)
    f.close()   

    operations = ['findone', 'insert', 'update', 'inplace_update']

    for op in operations:
        config['operation'] = op
        run_benchmark(config)

if __name__ == '__main__':
    sys.exit(main())
