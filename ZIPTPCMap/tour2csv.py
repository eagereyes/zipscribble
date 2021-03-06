#!/usr/bin/python

# Convert the tour file created by LKH into a CSV containing locations that can be
# drawn directly in Tableau or processed further.

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
import math

# distance calculation from http://www.math.uwaterloo.ca/tsp/world/geom.html
def distance(z1, z2):
	lati = math.pi * float(z1['lat']) / 180.
	latj = math.pi * float(z2['lat']) / 180.

	longi = math.pi * float(z1['lon']) / 180.
	longj = math.pi * float(z2['lon']) / 180.

	q1 = math.cos(latj) * math.sin(longi - longj)
	q3 = math.sin((longi - longj)/2.0)
	q4 = math.cos((longi - longj)/2.0)
	q2 = math.sin(lati + latj) * q3 * q3 - math.sin(lati - latj) * q4 * q4
	q5 = math.cos(lati - latj) * q4 * q4 - math.cos(lati + latj) * q3 * q3

	return int(6378388.0 * math.atan2(math.sqrt(q1*q1 + q2*q2), q5) + 1.0)

zipMap = [0]
with open('USzips.map', 'rb') as zipMapFile:
	csvMap = csv.reader(zipMapFile)

	for row in csvMap:
		zipMap.append({
			'zip': row[1],
			'lat': row[2],
			'lon': row[3],
			'state': row[4]
		})

tour = []
length = 0
previousZIP = None
with open('USzips.tour', 'rb') as tourFile:
	preamble = True
	count = 1
	for row in tourFile:
		if preamble:
			preamble = row.strip() != 'TOUR_SECTION'
		else:
			num = int(row)
			if num == -1:
				break
			
			z = zipMap[num]
			tour.append([count, z['zip'], z['lat'], z['lon'], z['state']])

			if count > 1:
				length += distance(z, previousZIP)
			
			previousZIP = z
			count += 1

print 'tour length: '+str(int(length))+'m'

with open('USTPCmap.csv', 'wb') as outFile:
	csvOut = csv.writer(outFile)

	csvOut.writerow(['sequence', 'zip', 'lat', 'lon', 'state'])
	csvOut.writerows(tour)
	csvOut.writerow(tour[0])
