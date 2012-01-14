#!/usr/bin/python

import csv
import json
import sys

def compare(a, b):
	return cmp(a['zip'], b['zip'])

reader = csv.reader(open(sys.argv[1], 'rb'), delimiter='\t')

zips = []
for row in reader:
	if len(row) > 10 and len(row[3]) > 0 and len(row[9]) > 0 and len(row[10]) > 0:
		z = {'zip':   row[1],
			 'lat':   float(row[9]),
			 'lon':   float(row[10]),
			 'state': row[4]
			 }
		zips.append(z)

zips.sort(compare)

last = zips[-1]
for i in range(len(zips)-2, -1, -1):
    if last['lon'] == zips[i]['lon'] and last['lat'] == zips[i]['lat']:
        del zips[i]
    else:
        last = zips[i]

geoJSON = {	'type': 'LineString' }

geoJSON['coordinates'] = map(lambda z : [z['lon'], z['lat']], zips)

country = sys.argv[1][:-4]

with open('zipscribble_'+country+'.json', 'wb') as out:
	json.dump(geoJSON, out)

state = ''
for zip in zips:
	if zip['state'] != state:
		state = zip['state']
		print state
