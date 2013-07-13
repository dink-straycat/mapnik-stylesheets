#!/usr/bin/python

# unit=m
pedestrian=2
service=2
residential=2
road=residential
unclassified=3
tertiary=5
secondary=6
primary=secondary
trunk=primary

# unit=px
case=2


d = {
    'moto-fill1': '#d6dfea',
    'seco-fill': '#fed7a5',
    'tert-fill1': '#ffc',
    'tert-fill2': '#ffffb3',
    'trc17': 1 * trunk + case,
    'trf17': 1 * trunk,
    'prc17': 1 * primary + case,
    'prf17': 1 * primary,
    'sec17': 1 * secondary + case,
    'sef17': 1 * secondary,
    'tec17': 1 * tertiary + case,
    'tef17': 1 * tertiary,
    'unc17': 1 * unclassified + case,
    'unf17': 1 * unclassified,
    'rec17': 1 * residential + case,
    'ref17': 1 * residential,
    'roc17': 1 * road + case,
    'rof17': 1 * road,
    'svc17': 1 * service + case,
    'svf17': 1 * service,
    'pec17': 1 * pedestrian + case,
    'pef17': 1 * pedestrian,
    'trc18': 2 * trunk + case,
    'trf18': 2 * trunk,
    'prc18': 2 * primary + case,
    'prf18': 2 * primary,
    'sec18': 2 * secondary + case,
    'sef18': 2 * secondary,
    'tec18': 2 * tertiary + case,
    'tef18': 2 * tertiary,
    'unc18': 2 * unclassified + case,
    'unf18': 2 * unclassified,
    'rec18': 2 * residential + case,
    'ref18': 2 * residential,
    'roc18': 2 * road + case,
    'rof18': 2 * road,
    'svc18': 2 * service + case,
    'svf18': 2 * service,
    'pec18': 2 * pedestrian + case,
    'pef18': 2 * pedestrian,
}

with open('osm-template.xml') as f:
    for line in f:
        print line.format(**d),
