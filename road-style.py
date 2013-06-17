#!/usr/bin/python

d = {
    'moto-fill1': '#d6dfea',
    'seco-fill': '#fed7a5',
    'tert-fill1': '#ffc',
    'tert-fill2': '#ffffb3',
}

with open('osm-template.xml') as f:
    for line in f:
        print line.format(**d),
