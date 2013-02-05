import sys
import csv
import utc
import xml.etree.cElementTree as ET


def convert(fp):
    rows = csv.reader(fp)
    rows.next()  # header

    root = ET.fromstring('<entities type="federal-body"></entities>')
    root.attrib['updated'] = utc.now_isoformat()

    for row in rows:
        eid, epid, ename, abbr, hist, leader = [c.decode('cp1252').strip() for c in row]
        entity = ET.SubElement(root, 'entity')
        entity.attrib['id'] = "{:0>4s}".format(eid)
        if epid:
            entity.attrib['parent-id'] = "{:0>4s}".format(epid) if epid else ''
        name = ET.SubElement(entity, 'name')
        name.set('role', 'official')
        name.text = ename
        if hist:
            name = ET.SubElement(entity, 'name')
            name.set('role', 'historical')
            name.text = hist
        if leader:
            name = ET.SubElement(entity, 'name')
            name.set('role', 'leadership')
            name.text = leader
        if abbr:
            name = ET.SubElement(entity, 'abbr')
            name.text = abbr

    return root

if __name__ == '__main__':
    ifn, ofn = sys.argv[1:3]
    with file(ifn, 'rU') as fp:
        root = convert(fp)
        ET.ElementTree(root).write(ofn, encoding='utf-8')
