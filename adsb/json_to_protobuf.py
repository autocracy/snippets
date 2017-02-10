#!/usr/bin/env python3
import gzip
import json
import sys

import adsb_pb2

from concurrent import futures

executor = futures.ProcessPoolExecutor()

def process_file(baseName):
    try:
        f = open('adsb/' + baseName)
        j = json.load(f)
        out = adsb_pb2.AcList()
        for plane in j['acList']:
            a = out.aircraft.add()
            for (k, v) in plane.items():
                if v == "":
                    continue
                if k == 'Cos':
                    a.Cos.extend([x for x in v if x != None])
                    continue
                if k == 'Stops':
                    a.Stops.extend(v)
                    continue
                if k == 'FSeen':
                    a.FSeen = int(''.join(list(filter(str.isdigit, v))))
                    continue
                if k in ('Spd', 'Sqk'):
                    v = int(v)
                setattr(a, k, v)
        with gzip.open('output/' + baseName, 'wb') as f:
            f.write(out.SerializeToString())
    except Exception as e:
        print(plane)
        raise

tasks = {executor.submit(process_file, filename): filename for filename in sys.argv[1:]}
#for filename in sys.argv[1:]:
#    process_file(filename)
