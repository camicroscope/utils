#!/usr/bin/env python3

import xml.etree.ElementTree as ET

# read and parse xml annotation
root = ET.parse('sample.xml').getroot()

# initialize output
features = []

for region in root.findall('Annotation/Regions/Region'):
    value = region.get('Id')
    print("Looking at Region Id", value)
    # initialize output for this region
    min_x = 99e99
    max_x = 0
    min_y = 99e99
    max_y = 0
    coordinates = []
    for region in region.findall('Vertices/Vertex'):
        value = region.get('X')
        # keep track of min and max x and y for bound
        min_x = min(min_x, float(region.get('X')))
        min_y = min(min_y, float(region.get('Y')))
        max_x = max(max_x, float(region.get('X')))
        max_y = max(max_y, float(region.get('Y')))
        # add the current coordinate
        coordinates.append([region.get('X'), region.get('Y')])
    # close polygon by re-adding first
    if len(coordinates):
        coordinates.append(coordinates[0])
        # make bound rect
        bound_rect = [[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y], [min_x, min_y]]
        # append output
        feature = {}
        feature['type'] = "Feature"
        feature['geometry'] = {}
        feature['geometry']['type'] = "Polygon"
        feature['geometry']['coordinates'] = [coordinates]
        feature['bound'] = {}
        feature['bound']['type'] = "Polygon"
        feature['bound']['coordinates'] = [bound_rect]
        features.append(feature)
    else:
        print("Empty of Vertices?")

if not len(features):
    sys.exit("Unable to read any features")
print(features)
