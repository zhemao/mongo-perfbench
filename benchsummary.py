#!/usr/bin/env python

# Generates a text summary of the results of the benchmark
# Usage: benchsummary.py [results.json]
# The first argument is a json file such as that created by mongoexport
# If no argument is given, the json will be read from standard input

import json
import sys

def total_ops(trial):
    """Calculate the total number of operations performed in this trial"""
    return sum(trial[op] for op in ['query', 'insert', 'update', 'delete'])

def summarize_data(data):
    """Print out a one line summary of this data point"""
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
