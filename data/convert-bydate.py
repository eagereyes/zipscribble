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

bydate = csv.reader(open('POdates_1700to1900.csv', 'rb'))

zips = []

lineNum = 0
for line in bydate:
	if lineNum > 0:
		year = line[0]
		lat = line[1]
		lon = line[2]
		if lat != '' and lon != '':
			zips.append(['US',year,'','','','','','','',lat,lon])
	
	lineNum += 1
	
txt = csv.writer(open('US-bydate.txt', 'w'), delimiter='\t')
txt.writerows(zips)
