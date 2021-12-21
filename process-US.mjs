
import { parse } from 'csv-parse/sync';
import { stringify } from 'csv-stringify';
import { bisector } from 'd3-array';
import { readFile, writeFile } from 'fs/promises';

const FNAME_GEONAMES = 'data/US.txt';
const FNAME_SIMPLEMAPS = 'srcdata/simplemaps_uszips_basicv1/uszips.csv'; // https://simplemaps.com/data/us-zips
const OUTFILENAME = 'scrbblr/public/data/us-lower48.csv';

const INCLUDES = ['AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
					'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
					'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ',
					'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD',
					'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'];


const gnCSV = await readFile(FNAME_GEONAMES);

let records = parse(gnCSV, { delimiter: '\t'});

let zips = [];

// console.log(records[0]);
for (let row of records) {
	if (INCLUDES.includes(row[4])) {
		const lon = +row[10];
		const lat = +row[9];
		// const p = project([lon, lat]);
		const z = {
			zip:		row[1],
			place:		row[2],
			state:		row[4],
			lon:		lon,
			gnLon:		lon,
			smLon:		lon,
			lat:		lat,
			gnLat:		lat,
			smLat:		lat,
			// lon_proj:	p[0],
			// lat_proj:	p[1]
		};
		zips.push(z);
	}
}

zips.sort((a, b) => a.zip-b.zip);

const zBisector = bisector(a => a.zip);

// console.log(zips.length);

const smCSV = await readFile(FNAME_SIMPLEMAPS);

records = parse(smCSV, { columns: true });

let matches = 0;

for (let row of records) {
	if (INCLUDES.includes(row.state_id)) {
		const zipIndex = zBisector.left(zips, row.zip);
		// console.log(row.zip, zipIndex, zips[zipIndex].zip);
		if (zipIndex < zips.length && zips[zipIndex].zip === row.zip) {
			zips[zipIndex].smLat = +row.lat;
			zips[zipIndex].smLon = +row.lng;
			matches += 1;
		} else {
			const z = {
				zip:		row.zip,
				place:		row.city,
				state:		row.state_id,
				lon:		+row.lng,
				smLon:		+row.lng,
				lat:		+row.lat,
				smLat:		+row.lat,
			};
				
			zips = zips.slice(0, zipIndex).concat(z).concat(zips.slice(zipIndex));
		}
	}
}

console.log(`${zips.length} filtered ZIP codes`);

let diffCnt = 0;

for (let z of zips) {
	if (Math.abs(z.smLat-z.gnLat) > .1 || Math.abs(z.smLon-z.gnLon) > .1) { // when in doubt, use SimpleMaps numbers
		z.lat = z.smLat;
		z.lon = z.smLon;
		// console.log(z);
		diffCnt += 1;
	}
}

console.log(`${diffCnt} mismatches`);

let duplicates = 0;
for (let i = 1; i < zips.length; i += 1) {
	if (zips[i-1].lat === zips[i].lat && zips[i-1].lon === zips[i].lon) {
		zips[i].duplicate = true;
		duplicates += 1;
	}
}

console.log(`${duplicates} duplicates`);

zips = zips.filter(z => !z.duplicate);

console.log(`${zips.length} unique ZIPs`);

stringify(zips, { header: true,
  	columns: [ {key: 'zip'}, {key: 'place'}, {key: 'state'}, {key: 'lat'}, {key: 'lon'} ] },
	(err, output) => {
			writeFile(OUTFILENAME, output);
			// console.log(output);
	});
