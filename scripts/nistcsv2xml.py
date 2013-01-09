import sys, csv, datetime
import xml.etree.cElementTree as ET

def convert(fp):
    rows = csv.reader(fp)
    rows.next() #header
    
    root = ET.fromstring('<entities type="federal-entity"></entities>')
    root.attrib['updated'] = datetime.datetime.now().replace(microsecond=0).isoformat()
    
    for row in rows:
        eid, epid, ename = [c.decode('cp1252').strip() for c in row]
        entity = ET.SubElement(root, 'entity')
        entity.attrib['id'] = "{:0>4s}".format(eid)
        if epid:
            entity.attrib['parent-id'] = "{:0>4s}".format(epid) if epid else ''
        name = ET.SubElement(entity, 'name')
        name.set('role', 'official')
        name.text = ename
    return root

if __name__=='__main__':
    ifn, ofn = sys.argv[1:3]
    with file(ifn, 'rU') as fp:
        root = convert(fp)
        ET.ElementTree(root).write(ofn, encoding='utf-8')
        