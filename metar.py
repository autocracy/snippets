import re

records = []
with open('metar') as f:
    record = ''
    keep = False
    for line in f.readlines():
        if line[0] == '2':
           if keep:
               records.append(record)
           if line[13:18] == 'METAR':
                record = line.rstrip()
                keep = True
           else:
                keep = False
        if line[0] == ' ':
            record += ' ' + line.lstrip().rstrip()

for r in records:
    t = "-".join([r[0:4], r[4:6], r[6:8]]) + " " + ":".join([r[8:10], r[10:12]])
    l = r[19:23]
    try:
        v = re.search('1?(\d \d/)?\d(?= ?SM)', r).group(0)
    except:
        """ Visibility must be missing or broken """
        continue 
    if re.search('/', v):
        v = str(int(v[0]) + float(v[2]) / float(v[4]))
    print("\t".join([t, l, v]))

#print("\n".join(records))
