#!/usr/bin/env python
# encoding: utf-8
"""
doctypes2xml.py

Create billversions.xml describing bill version suffixes from doctypes.txt

Created by Francis Avila on 2012-08-03.
Copyright (c) 2012 Dancing Mammoth, Inc. All rights reserved.
"""

import sys
import xml.etree.cElementTree as ET
from collections import namedtuple
from datetime import datetime

billversionfields = "version id definition chambers"
BillVersion = namedtuple('BillVersion', billversionfields)



def groupLines(lines):
    # import pdb; pdb.set_trace()
    fields = BillVersion._fields
    chambers = {'House':'H', 'Senate':'S'}
    group = []
    chambergroup = []
    normalfields = len(fields)-1
    for line in lines:
        line = line.strip().decode('utf-8')
        if len(group) >= normalfields:
            if line in chambers:
                chambergroup.append(chambers[line])
            else:
                group.append(tuple(chambergroup))
                bv = BillVersion._make(group)
                group = [line]
                chambergroup = []
                yield bv
        else:
            group.append(line)


def doc2xml(billversions):
    billversionET = ET.Element("entities",
        type="billversion",
        description="Definitions of Common Versions of Bills",
        source="http://www.gpo.gov/help/about_congressional_bills.htm",
        updated=datetime.today().replace(microsecond=0).isoformat())
    
    for bill in billversions:
        d = bill._asdict()
        d['chambers'] = ' '.join(sorted(d['chambers']))
        version = d['version']
        del d['version']
        bv = ET.SubElement(billversionET, 'entity', **d)
        ET.SubElement(bv, 'name', role="official").text = version
        
    return billversionET

def main():
    inf, of = sys.argv[1], sys.argv[2]
    with open(inf, 'rb') as f:
        billversions = groupLines(f)
        billversions = doc2xml(billversions)
    ET.ElementTree(billversions).write(of, encoding='utf-8')

if __name__ == "__main__":
    main()
