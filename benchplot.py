#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
import sys

def total_ops(trial):
    return sum(trial[op] for op in ['query', 'insert', 'update', 'delete'])

def summarize_data(data):
    name = data['name']
    numThreads = data['numThreads']
    numTrials = data['numTrials']
    avgops = sum([total_ops(trial) for trial in data['trials']]) / numTrials
    avglat = sum([trial[name + 'LatencyAverageMs'] 
                    for trial in data['trials']]) / numTrials
                    
    return numThreads, avgops, avglat

    #return '%s\t\t%d\t\t%6d\t\t%6d' % (name, numThreads, avgops, avglat)

def main():
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    else:
        f = sys.stdin

    #print 'test name\t# threads\tavg operations\tavg latency (us)'
    
    allThreads = []
    allOps = []
    allLatency = []

    for line in f:
        data = json.loads(line.strip())
        threads, ops, lat = summarize_data(data)
        allThreads.append(threads)
        allOps.append(ops)
        allLatency.append(lat)
        
        #print summarize_data(data)
    
    plt.figure(1)
    
    plt.subplot(311)
    plt.xlabel('Threads')
    plt.ylabel('Number of Ops/sec')
    plt.plot(allThreads, allOps)
    
    plt.subplot(312)
    plt.xlabel('Threads')
    plt.ylabel('Latency(micros)')
    plt.plot(allThreads, allLatency)
    
    plt.subplot(313)
    plt.ylabel('Latency(micros)')
    plt.xlabel('Ops/sec')
    plt.plot(allOps, allLatency, 'r:')
    plt.show()

if __name__ == '__main__':
    main()
