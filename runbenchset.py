from runbench import run_benchmark
import json
import sys

def main():
    if len(sys.argv) < 2:
        return "Usage: " + sys.argv[0] + ' configfile.json'

    f = open(sys.argv[1])
    config = json.load(f)
    f.close()   

    operations = ['findone', 'insert', 'update', 'inplace_update']

    for op in operations:
        config['operation'] = op
        run_benchmark(config)

if __name__ == '__main__':
    sys.exit(main())
