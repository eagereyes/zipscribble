<script>
	import { text } from 'd3-fetch';
	import { geoAlbers } from 'd3-geo';

	import ZIPScribble from './ZIPScribble.svelte';
	import PlacesBars from './PlacesBars.svelte';

	const FILENAME = 'data/US.txt';
	const EXCLUDES = ['AA', 'AK', 'AP', 'HI', 'GU', 'FM', 'PW', 'MP', 'MH'];
	const PROJECTION = geoAlbers();

	const SVGWIDTH = 800;
	const SVGHEIGHT = 600;

	let zipCodes = null;
	let places = [];

	let range = [];

	text(FILENAME).then(data => {
		let records = data.split('\n');
		let zips = [];
		for (let r of records) {
			let row = r.split('\t');
			if (!EXCLUDES.includes(row[4]) && row.length > 1) {
				const lon = +row[10];
				const lat = +row[9];
				const p = PROJECTION([lon, lat]);
				let z = {
					zip:		+row[1],
					place:		row[2],
					state:		row[4],
					lon:		+lon,
					lat:		+lat,
					lon_proj:	p[0],
					lat_proj:	p[1]
				};
				zips.push(z);
			}
		}

		zips.sort((a, b) => a.zip-b.zip);

		console.log(`${zips.length} ZIP codes`);

		zipCodes = zips;

		let placeHash = {};

		for (let z of zips) {
			const p = `${z.place}, ${z.state}`;
			if (p in placeHash) {
				placeHash[p].zips += 1;
			} else {
				placeHash[p] = {
					name: p,
					firstZIP: z.zip,
					zips: 1
				}
			}
		}

		places = Object.values(placeHash);

		places.sort((a, b) => b.zips - a.zips);
	});

</script>

<main>
	<svg width={SVGWIDTH} height={SVGHEIGHT}>
		<ZIPScribble width={SVGWIDTH} height={SVGHEIGHT-50} {zipCodes}
			{range} />
		<PlacesBars y={SVGHEIGHT-50} height={50} width={SVGWIDTH}
			places={places.filter(p => p.zips > 20)} bind:range={range} />
	</svg>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>