#!/usr/bin/env python3
import argparse
import xml.etree.ElementTree as ET
import json

# arguments
parser = argparse.ArgumentParser(description='xml to geojson annotation converter')
parser.add_argument('input', nargs=1, help='Filepath for XML input')
parser.add_argument('output', nargs='?', default=False, help='Filepath for json output')
args = parser.parse_args()
print(args)
# read and parse xml annotation
root = ET.parse(args.input[0]).getroot()

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
        x = float(region.get("X"))
        y = float(region.get("Y"))
        # keep track of min and max x and y for bound
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        # add the current coordinate
        coordinates.append([x, y])
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

if (args.output):
    # write file
    with open(args.output, 'w') as json_file:
        json.dump(features, json_file)
else:
    print(features)
