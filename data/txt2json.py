#!/usr/bin/python

#	Copyright (c) 2012, Robert Kosara <rkosara@me.com>
#	
#	Permission to use, copy, modify, and/or distribute this software for any
#	purpose with or without fee is hereby granted, provided that the above
#	copyright notice and this permission notice appear in all copies.
#	
#	THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#	WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#	MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#	ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#	WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#	ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#	OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import csv
import json
import sys
import os

def compare(a, b):
	return cmp(a['zip'], b['zip'])

countryInfo = {}

def convertCountry(country, sortZIPs):

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
			((country == 'US' and len(row[3]) > 0) or country != 'US') and
			((country == 'RU' and float(row[10]) > 0) or country != 'RU') and
			((country == 'CA' and float(row[9]) < 90) or country != 'CA')):
			z = {'zip':   row[1],
				 'lat':   float(row[9]),
				 'lon':   float(row[10]),
				 'state': row[4] if len(row[4]) > 0 else 'None' 
				 }
			zips.append(z)

#			if country == 'RU' and z['lon'] < 0:
#				z['lon'] = 180 - z['lon']

			if not z['state'] in states:
				states[z['state']] = []

			if not ((country == 'US' and (z['lat'] > 50 or z['lon'] < -125)) or
				((country == 'ES' or country == 'PT') and z['lat'] < 35) or
				(country == 'FR' and z['lon'] < -7)):

				boundingbox['minLat'] = min(boundingbox['minLat'], z['lat'])
				boundingbox['maxLat'] = max(boundingbox['maxLat'], z['lat'])
				boundingbox['minLon'] = min(boundingbox['minLon'], z['lon'])
				boundingbox['maxLon'] = max(boundingbox['maxLon'], z['lon'])
	
	centerLat = (boundingbox['minLat'] + boundingbox['maxLat'])/2;
	centerLon = (boundingbox['minLon'] + boundingbox['maxLon'])/2;

	countryInfo[country] = { 'bbox':
		[{'lon': centerLon - (centerLon - boundingbox['minLon']) * 1.1,
		 'lat': centerLat - (centerLat - boundingbox['minLat']) * 1.1},
		{'lon': centerLon + (boundingbox['maxLon'] - centerLon) * 1.1,
		 'lat': centerLat + (boundingbox['maxLat'] - centerLat) * 1.1}]
	}
		 
	if len(zips) == 0:
		print 'No data for '+country+'!'
	else:
	
		if sortZIPs:
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
			
			countryInfo[country]['states'] = False
			
		else:
		
			stateConnectors = []

			previousState = None
			previousPoint = None
			for zip in zips:
				if zip['state'] != previousState:
					previousState = zip['state']
					states[previousState].append([])
					if previousPoint != None:
						stateConnectors.append(
							[previousPoint['lon'], previousPoint['lat']])
						stateConnectors.append([zip['lon'], zip['lat']])
					
				states[previousState][-1].append([zip['lon'], zip['lat']])
				previousPoint = zip

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
		
			geoJSON['features'].insert(0, {
				'type': 'Feature',
				'geometry': {
					'type': 'LineString',
					'coordinates': stateConnectors
				},
				'properties': {},
				'id': '000stateconnectors'
			})
	
			countryInfo[country]['states'] = True
	
		
		with open('zipscribble_'+country+'.json', 'wb') as out:
			json.dump(geoJSON, out)		



for file in os.listdir('.'):
	if len(file) == 6 and file[-4:] == '.txt':
		country = file[:2]
		print country
		convertCountry(country, True)

print 'US-bydate'
convertCountry('US-bydate', False)

with open('countryinfo.json', 'wb') as info:
	json.dump(countryInfo, info)
