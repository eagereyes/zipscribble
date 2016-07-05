#!/usr/bin/python

# Convert all the ZIP code tab-separated files to geoJSON that can be used on the web

#	Copyright (c) 2012-2016, Robert Kosara <rkosara@me.com>
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

# Parses the geonames ZIP code location file and returns a list of ZIP items and a list of states
def parseZIPsFile(country):
	reader = csv.reader(open('data/'+country+'.txt', 'rb'), delimiter='\t')

	states = {}
	zips = []
	for row in reader:
		if (len(row) > 10 and len(row[9]) > 0 and len(row[10]) > 0 and
			((country == 'US' and (len(row[3]) > 0 and row[1] != '96898')) or country != 'US') and # exclude Guam and Wake Island
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

	return (zips, states)

def parseTPCFile(filename):
	reader = csv.DictReader(open(filename, 'rb'))

	zips = []
	for row in reader:
		row['lat'] = float(row['lat'])
		row['lon'] = float(row['lon'])
		zips.append(row)
	
	return zips

def convertCountry(country, zips, states, sortZIPs):

	boundingbox = {	'minLat': 10000,
					'maxLat': -10000,
					'minLon': 10000,
					'maxLon': -10000
					}

	for z in zips:
		if not ((country[:2] == 'US' and (z['lat'] > 50 or z['lon'] < -125)) or
			((country == 'ES' or country == 'PT') and z['lat'] < 35) or
			(country == 'FR' and z['lon'] < -7)):

			boundingbox['minLat'] = min(boundingbox['minLat'], z['lat'])
			boundingbox['maxLat'] = max(boundingbox['maxLat'], z['lat'])
			boundingbox['minLon'] = min(boundingbox['minLon'], z['lon'])
			boundingbox['maxLon'] = max(boundingbox['maxLon'], z['lon'])
	
	centerLat = (boundingbox['minLat'] + boundingbox['maxLat'])/2;
	centerLon = (boundingbox['minLon'] + boundingbox['maxLon'])/2;

	countryInfo[country] = { 'bbox':
		[boundingbox['minLon'], boundingbox['maxLon'], boundingbox['minLat'], boundingbox['maxLat']]
	}
	
	print countryInfo[country]['bbox'];

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
		
		# fake states consisting of 1000 zip codes each
		stateNum = 1;
		counter = 0;
		states = {}
		states['s'+str(stateNum)] = []
		for z in zips:
			z['state'] = 's'+str(stateNum)
			counter += 1
			if counter == 1000:
				stateNum += 1
				states['s'+str(stateNum)] = []
				counter = 0

		if len(states.keys()) == 1:
			geoJSON = {
				'type': 'LineString',
				'bbox': countryInfo[country]['bbox']
			}
			
			geoJSON['coordinates'] = map(lambda z : [z['lon'], z['lat']], zips)
			
			countryInfo[country]['states'] = False
			
		else:
		
			stateConnectors = []

			previousState = None
			previousPoint = None
			for zip in zips:
				if zip['state'] != previousState:
					if previousState != None:
						states[previousState].append([zip['lon'], zip['lat']])
					previousState = zip['state']
					
				states[previousState].append([zip['lon'], zip['lat']])
				previousPoint = zip

			geoJSON = {
				'type': 'FeatureCollection',
				'bbox': countryInfo[country]['bbox']
			}
			
			geoJSON['features'] = map(lambda s :
				{'type': 'Feature',
				 'geometry': {
				 	'type': 'LineString',
				 	'coordinates': states[s]
				 },
				 'properties': {},
				 'id': s
				}, states.keys())
		
			# geoJSON['features'].insert(0, {
			# 	'type': 'Feature',
			# 	'geometry': {
			# 		'type': 'LineString',
			# 		'coordinates': stateConnectors
			# 	},
			# 	'properties': {},
			# 	'id': '000stateconnectors'
			# })
	
			countryInfo[country]['states'] = True
	
		
		with open('data/zipscribble_'+country+'.json', 'wb') as out:
			json.dump(geoJSON, out)		



for file in os.listdir('data'):
	if len(file) == 6 and file[-4:] == '.txt':
		country = file[:2]
		print country
		zips, states = parseZIPsFile(country)
#		convertCountry(country, zips, states, True)
		# pretend we have no states, to see if that reduces artifacts
		convertCountry(country, zips, {country: []}, True)


zips = parseTPCFile('ZIPTPCMap/USTPCmap.csv')
convertCountry('USTPC', zips, {'US': []}, False)

with open('data/countryinfo.json', 'wb') as info:
	json.dump(countryInfo, info)
