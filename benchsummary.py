#!/usr/bin/env python

import json
import sys

def total_ops(trial):
    return sum(trial[op] for op in ['query', 'insert', 'update', 'delete', 'command'])

def summarize_data(data):
    name = data['name']
    numThreads = data['numThreads']
    numTrials = data['numTrials']
    avgops = sum([total_ops(trial) for trial in data['trials']]) / numTrials
    avglat = sum([trial[name + 'LatencyAverageMs'] 
                    for trial in data['trials']]) / numTrials

    return '%s\t\t%d\t\t%6d\t\t%6d' % (name, numThreads, avgops, avglat)

def main():
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    else:
        f = sys.stdin

    print 'test name\t# threads\tavg operations\tavg latency (us)'

    for line in f:
        data = json.loads(line.strip())
        print summarize_data(data)

if __name__ == '__main__':
    main()
