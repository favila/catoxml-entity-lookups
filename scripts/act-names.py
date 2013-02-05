#! /bin/python
# convert act names table to xml lookup table

import sys
import csv
import utc
import xml.etree.cElementTree as ET


def normalize_name(name):
    return name.replace('``', '"').replace("''", '"')


def convert(infile, outfile):
    reader = csv.reader(infile)
    reader.next()             # discard header

    acts = ET.Element('entities',
        type="act",
        updated=utc.now_isoformat()
    )

    for row in reader:
        row = [c.decode('CP1252').strip() for c in row]
        row = map(normalize_name, row)
        act = ET.SubElement(acts, 'entity', id=row[0])
        name = ET.SubElement(act, 'name')
        name.text = row[0]
        for extraname in row[2:]:
            if extraname:
                name = ET.SubElement(act, 'name')
                name.text = extraname

    lookup = ET.ElementTree(acts)
    lookup.write(outfile, encoding="utf-8")

if __name__ == '__main__':
    with open(sys.argv[1], 'rbU') as infile, open(sys.argv[2], 'wb') as outfile:
        convert(infile, outfile)
