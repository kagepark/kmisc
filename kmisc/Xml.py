#Kage Park

import xml.etree.ElementTree as ET

def findXML(xmlfile,find_name=None,find_path=None):
    tree=ET.parse(xmlfile)
    #root=ET.fromstring(data)
    root=tree.getroot()
    def find(tr,find_name):
        for x in tr:
            if x.attrib.get('name') == find_name:
                return x,x.tag
            rt,pp=find(x,find_name)
            if rt:
                return rt,'{}/{}'.format(x.tag,pp)
        return None,None
    found_root=None
    if find_name:
        found=find(root,find_name)
        if found[0]:
             found_root=found[0]
    if find_path and isinstance(find_path,str):
        #ex: root.findall('./Menu/Setting/[@name="Administrator Password"]/Information/HasPassword'):
        if not found_root: found_root=root
        return found_root.findall(find_path)
        # <element>.tag: name, .text: data, .attrib: dict

