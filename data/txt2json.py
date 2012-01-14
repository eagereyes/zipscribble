#!/usr/bin/python

import csv
import json
import sys
import os

def compare(a, b):
	return cmp(a['zip'], b['zip'])

boundingboxes = {}

def convertCountry(country):
	
	reader = csv.reader(open(country+'.txt', 'rb'), delimiter='\t')

	boundingbox = {	'minLat': 10000,
					'maxLat': -10000,
					'minLon': 10000,
					'maxLon': -10000
					}

	states = {}
	zips = []
	for row in reader:
		if (len(row) > 10 and len(row[9]) > 0 and len(row[10]) > 0 and
			((country == 'US' and len(row[3]) > 0) or country != 'US')):
			z = {'zip':   row[1],
				 'lat':   float(row[9]),
				 'lon':   float(row[10]),
				 'state': row[4] if len(row[4]) > 0 else 'None' 
				 }
			zips.append(z)

			if not z['state'] in states:
				states[z['state']] = []

			boundingbox['minLat'] = min(boundingbox['minLat'], z['lat'])
			boundingbox['maxLat'] = max(boundingbox['maxLat'], z['lat'])
			boundingbox['minLon'] = min(boundingbox['minLon'], z['lon'])
			boundingbox['maxLon'] = max(boundingbox['maxLon'], z['lon'])
	
	centerLat = (boundingbox['minLat'] + boundingbox['maxLat'])/2;
	centerLon = (boundingbox['minLon'] + boundingbox['maxLon'])/2;

	boundingboxes[country] = [
		{'lon': centerLon - (centerLon - boundingbox['minLon']) * 1.1,
		 'lat': centerLat - (centerLat - boundingbox['minLat']) * 1.1},
		{'lon': centerLon + (boundingbox['maxLon'] - centerLon) * 1.1,
		 'lat': centerLat + (boundingbox['maxLat'] - centerLat) * 1.1}]
	
	if len(zips) == 0:
		print 'No data for '+country+'!'
	else:
		zips.sort(compare)
		
		# uniq
		last = zips[-1]
		for i in range(len(zips)-2, -1, -1):
		    if last['lon'] == zips[i]['lon'] and last['lat'] == zips[i]['lat']:
		        del zips[i]
		    else:
		        last = zips[i]
		
		if len(states.keys()) == 1:
			geoJSON = {	'type': 'LineString' }
			
			geoJSON['coordinates'] = map(lambda z : [z['lon'], z['lat']], zips)
			
		else:
		
			previousState = ''
			for zip in zips:
				if zip['state'] != previousState:
					previousState = zip['state']
					states[previousState].append([])
				if previousState == '':
					print zip
				states[previousState][-1].append([zip['lon'], zip['lat']])
			
			geoJSON = {'type': 'FeatureCollection'}
			
			geoJSON['features'] = map(lambda s :
				{'type': 'Feature',
				 'geometry': {
				 	'type': 'MultiLineString',
				 	'coordinates': states[s]
				 },
				 'properties': {},
				 'id': s
				}, states.keys())
		
		with open('zipscribble_'+country+'.json', 'wb') as out:
			json.dump(geoJSON, out)		


for file in os.listdir('.'):
	if len(file) == 6 and file[-4:] == '.txt':
		country = file[:2]
		print country
		convertCountry(country)

with open('boundingboxes.json', 'wb') as bb:
	json.dump(boundingboxes, bb)
