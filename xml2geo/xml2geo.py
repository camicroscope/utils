#!/usr/bin/env python3

import xml.etree.ElementTree as ET
root = ET.parse('sample.xml').getroot()
print(root)
for region in root.findall('Annotation/Regions/Region'):
    value = region.get('Id')
    print("Region", value)
    for region in region.findall('Vertices/Vertex'):
        value = region.get('X')
        print(region.get('X'), region.get('Y'))
