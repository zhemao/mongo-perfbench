#!/usr/bin/env python

import json
import sys

name_to_op = {
    'findOne': 'query',
    'insert': 'insert',
    'update': 'update',
    'inplaceUpdate': 'update',
}

def summarize_data(data):
    name = data['name']
    op = name_to_op[name]
    numThreads = data['numThreads']
    numTrials = data['numTrials']
    avg = sum([trial[op] for trial in data['trials']]) / numTrials

    return '%s\t\t%d\t\t%f' % (name, numThreads, avg)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    else:
        f = sys.stdin

    print 'test name\t# threads\tavg latency'

    for line in f:
        data = json.loads(line.strip())
        print summarize_data(data)
