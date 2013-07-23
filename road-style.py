#!/usr/bin/python

# unit=m
pedestrian=2.0
service=2.0
residential=2.0
road=residential
unclassified=3.0
tertiary=5.0
secondary=6.0
primary=secondary
trunk=primary

# unit=px
case=2.0


d = {
    'moto-fill1': '#d6dfea',
    'seco-fill': '#fed7a5',
    'tert-fill1': '#ffc',
    'tert-fill2': '#ffffb3',
}

# zoomlevel 20 to 13
for z in range(8):
    zoomlevel = str(20 - z)
    width = 8.0 / ( 2 ** z )
    d['trc' + zoomlevel] = width * trunk + case
    d['trf' + zoomlevel] = width * trunk
    d['prc' + zoomlevel] = width * primary + case
    d['prf' + zoomlevel] = width * primary
    d['sec' + zoomlevel] = width * secondary + case
    d['sef' + zoomlevel] = width * secondary
    d['tec' + zoomlevel] = width * tertiary + case
    d['tef' + zoomlevel] = width * tertiary
    d['unc' + zoomlevel] = width * unclassified + case
    d['unf' + zoomlevel] = width * unclassified
    d['rec' + zoomlevel] = width * residential + case
    d['ref' + zoomlevel] = width * residential
    d['roc' + zoomlevel] = width * road + case
    d['rof' + zoomlevel] = width * road
    d['svc' + zoomlevel] = width * service + case
    d['svf' + zoomlevel] = width * service
    d['pec' + zoomlevel] = width * pedestrian + case
    d['pef' + zoomlevel] = width * pedestrian

with open('osm-template.xml') as f:
    for line in f:
        print line.format(**d),
