from collections import defaultdict
from concurrent import futures
import itertools
import gzip
import json
import sys

mastercount = defaultdict(lambda: 0)
exec = futures.ProcessPoolExecutor()

def cant_pickle_lambda():
    # Oh yeah, this is annoying...
    return 0

def processfile(filename):
    r = defaultdict(cant_pickle_lambda)
    f = gzip.open(filename)
    j = json.loads(str(f.read(), encoding='utf-8'))
    for ac in j['acList']:
        for key in ac.keys():
            r[key] = r[key] + 1
    return r

tasks = {exec.submit(processfile, filename): filename for filename in sys.argv[1:]}
for future in futures.as_completed(tasks):
    filecount = future.result()
    for (k, v) in filecount.items():
        mastercount[k] = mastercount[k] + v
print(mastercount) 
