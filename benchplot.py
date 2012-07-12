#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import sys

def total_ops(trial):
    """Calculate the total number of operations performed in this trial"""
    return sum(trial[op] for op in ['query', 'insert', 'update', 'delete'])

def summarize_data(data):
    """Calculate and return the number of threads, the average number of
    operations performed, and the average latency."""
    name = data['name']
    numThreads = data['numThreads']
    numTrials = data['numTrials']
    avgops = sum([total_ops(trial) for trial in data['trials']]) / numTrials
    avglat = sum([trial[name + 'LatencyAverageMs'] 
                    for trial in data['trials']]) / numTrials
                    
    return numThreads, avgops, avglat

def main():
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    else:
        f = sys.stdin

    allThreads = []
    allOps = []
    allLatency = []

    # go through and append the thread #, ops, and latency 
    # to the proper lists
    for line in f:
        data = json.loads(line.strip())
        threads, ops, lat = summarize_data(data)
        allThreads.append(threads)
        allOps.append(ops)
        allLatency.append(lat)
    
    plt.figure(1)
    
    # plot operations vs threads
    plt.subplot(311)
    plt.xlabel('Threads')
    plt.ylabel('Number of Ops/sec')
    plt.plot(allThreads, allOps)
    
    # plot latency vs threads
    plt.subplot(312)
    plt.xlabel('Threads')
    plt.ylabel('Latency(micros)')
    plt.plot(allThreads, allLatency)
    
    # plot latency vs operations
    plt.subplot(313)
    plt.ylabel('Latency(micros)')
    plt.xlabel('Ops/sec')
    plt.plot(allOps, allLatency, 'r:')
    plt.show()

if __name__ == '__main__':
    main()
