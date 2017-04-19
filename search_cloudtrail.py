from collections import defaultdict
from concurrent import futures
import gzip
import json
import sys
import os

exec = futures.ProcessPoolExecutor()

def processfile(filename):
    trail = []
    f = gzip.open(filename)
    j = json.loads(str(f.read(), encoding='utf-8'))
    for record in j["Records"]:
        if "TEXT_STRING_DESIRED" in str(record):
            trail.append(record)
    return trail
    
tasks = []
for dirpath, dirnames, filenames in os.walk('trail'):
    for f in filenames:
        tasks.append(exec.submit(processfile, os.path.join(dirpath, f)))

trail = []
for f in futures.as_completed(tasks):
    trail.extend(f.result())
print(trail)
