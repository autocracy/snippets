#!/usr/bin/env python3
import gzip
import json
import sys
import zipfile
import avro.schema

from concurrent import futures
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

executor = futures.ProcessPoolExecutor()
schema = avro.schema.Parse(open("adsb.avsc").read())

def load_json(name):
    with z.open(name) as data:
        j = json.loads(data.read().decode("utf-8"))
    return j

def sanitize(json_data):
    a = {}
    for (k, v) in json_data.items():
        if v == "":
            continue
        if k == 'Cos':
            a['Cos'] = [x for x in v if x != None]
            continue
        if k == 'FSeen':
            v = int(''.join(list(filter(str.isdigit, v))))
            continue
        if k in ('Spd', 'Sqk'):
            v = int(v)
        a[k] = v
    return a

def process_file(fname):
    data = load_json(fname)
    writer = DataFileWriter(gzip.open(fname + ".avro.gz", "wb"), DatumWriter(), schema)
    for aircraft in data['acList']:
        writer.append(sanitize(aircraft))
    writer.close()

z = zipfile.ZipFile(sys.argv[1])
targets = z.namelist()
tasks = {executor.submit(process_file, filename): filename for filename in targets}
