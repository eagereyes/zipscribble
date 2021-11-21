
import { parse } from 'csv-parse';
import { stringify } from 'csv-stringify';
import { readFile, writeFile } from 'fs/promises';
import { geoAlbers } from 'd3-geo';

const FILENAME = 'data/US.txt';

const EXCLUDES = ['AA', 'AK', 'AP', 'HI', 'GU', 'FM', 'PW', 'MP', 'MH'];

const project = geoAlbers();

const csvContent = await readFile(FILENAME);

parse(csvContent, {
	delimiter: '\t'
	}, function(err, records){
		// console.log(records[0]);
		let zips = [];
		for (let row of records) {
			if (!EXCLUDES.includes(row[4])) {
				const lon = +row[10];
				const lat = +row[9];
				const p = project([lon, lat]);
				let z = {
					zip:		row[1],
					place:		row[2],
					state:		row[4],
					lon:		lon,
					lat:		lat,
					lon_proj:	p[0],
					lat_proj:	p[1]
				};
				zips.push(z);
			}
		}

		zips.sort((a, b) => a.zip-b.zip);

		stringify(zips, (err, output) => {
			output = 'ZIP,Place,State,Longitude,Latitude,Longitude_Projected,Latitude_Projected\n'+output;
			writeFile('us-projected-lower48.csv', output);
			// console.log(output);
		});

		console.log(`${zips.length} ZIP codes`);

		let places = {};

		for (let z of zips) {
			const p = `${z.place}, ${z.state}`;
			if (p in places) {
				places[p].zips += 1;
			} else {
				places[p] = {
					name: p,
					firstZIP: z.zip,
					zips: 1
				}
			}
		}

		let placesList = Object.values(places);

		placesList.sort((a, b) => b.zips - a.zips);

		stringify(placesList, (err, output) => {
			output = 'Place,FirstZIP,Count\n'+output;
			writeFile('us-lower48-zipcounts.csv', output);
			// console.log(output);
		});

	});
