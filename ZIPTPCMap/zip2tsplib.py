#!/usr/bin/python

# Create a TSPLIB file from the U.S. ZIP code data to run LKH or Concorde on.
# This script does some fairly extensive checking to remove duplicates by location,
# even when they're not consecutive by ZIP code.
# Also, this is lower-48 only

#	Copyright (c) 2016, Robert Kosara <rkosara@me.com>
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

reader = csv.reader(open('../data/US.txt', 'rb'), delimiter='\t')

def compare(a, b):
	return cmp(a['zip'], b['zip'])

zips = []
for row in reader:
	if len(row) > 10 and len(row[9]) > 0 and len(row[10]) > 0 and len(row[3]) > 0 and row[1] != '96898':

		z = {'zip':		row[1],
			 'lat':		float(row[9]),
			 'lon':		float(row[10]),
			 'strlat':	row[9],
			 'strlon':	row[10],
			 'state':	row[4] if len(row[4]) > 0 else 'None' 
			}

		if z['lat'] < 50 and z['lon'] > -125:
			zips.append(z)

# sort
zips.sort(compare)

# uniq
last = zips[-1]
for i in range(len(zips)-2, -1, -1):
	repeat = False
	for j in range(i+1, min(i+10, len(zips))):
		repeat |= zips[i]['lon'] == zips[j]['lon'] and zips[i]['lat'] == zips[j]['lat']
	if last['zip'] == zips[i]['zip'] or repeat:
		del zips[i]
	else:
		last = zips[i]

with open('USzips.tsp', 'wb') as tspFile:
	with open('USzips.map', 'wb') as mapFile:
		tspFile.write('NAME: USzips\n')
		tspFile.write('COMMENT: U.S. Traveling Presidential Candidate Map\n')
		tspFile.write('TYPE: TSP\n')
		tspFile.write('DIMENSION: '+str(len(zips))+'\n')
		tspFile.write('EDGE_WEIGHT_TYPE: EUC_2D\n')
		tspFile.write('NODE_COORD_SECTION\n')
		num = 1
		for z in zips:
			tspFile.write(str(num)+' '+str(z['lat']*1000.)+' '+str(z['lon']*1000.)+'\n')
			mapFile.write(str(num)+','+z['zip']+','+z['strlat']+','+z['strlon']+','+z['state']+'\n')		
			num += 1

		tspFile.write('EOF\n');
