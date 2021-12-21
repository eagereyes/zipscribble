<script>
	import { csv, text } from 'd3-fetch';
	import { geoAlbers } from 'd3-geo';
	import { onMount } from 'svelte';

	import ZIPScribble from './ZIPScribble.svelte';
	import PlacesBars from './PlacesBars.svelte';
	import Navigator from './Navigator.svelte';

	// const FILENAME = 'data/US.txt';
	const FILENAME = 'data/us-lower48.csv';
	const PROJECTION = geoAlbers();

	const SVGWIDTH = 800;
	const SVGHEIGHT = 600;

	let zipCodes = null;
	let places = [];
	let digits = [...Array(10)].map(d => {
					return {
						startOffset:	0,
						endOffset:		0,
						states:			[],
						secondDigits:	[...Array(10)].map(d => {
											return {
												startOffset:	0,
												endOffset:		0,
											}})
					}});

	let zoomRange = [];
	let highlightRange = [];

	onMount(async () => {
		// text(FILENAME).then(data => {
		// 	let records = data.split('\n');
		// 	let zips = [];
		// 	for (let r of records) {
		// 		let row = r.split('\t');
		// 		if (!EXCLUDES.includes(row[4]) && row.length > 1) {
		// 			const lon = +row[10];
		// 			const lat = +row[9];
		// 			const p = PROJECTION([lon, lat]);
		// 			let z = {
		// 				zip:		+row[1],
		// 				place:		row[2],
		// 				state:		row[4],
		// 				lon:		+lon,
		// 				lat:		+lat,
		// 				lon_proj:	p[0],
		// 				lat_proj:	p[1]
		// 			};
		// 			zips.push(z);
		// 		}
		// 	}

		// 	zips.sort((a, b) => a.zip-b.zip);

		csv(FILENAME).then(zips => {

			for (let z of zips) {
				const p = PROJECTION([z.lon, z.lat]);
				z.lon_proj = p[0];
				z.lat_proj = p[1];
			}

			let currentDigit = 0;
			let currentSecondDig = 0;
			let prevState = '';
			for (let rowNum = 0; rowNum < zips.length; rowNum += 1) {
				let z = zips[rowNum];
				if (Math.floor(z.zip/10000) > currentDigit) {
					digits[currentDigit].states[digits[currentDigit].states.length-1].endOffset = rowNum;
					digits[currentDigit].endOffset = rowNum;
					digits[currentDigit].secondDigits[currentSecondDig].endOffset = rowNum;
					currentDigit = Math.floor(z.zip/10000);
					digits[currentDigit].startOffset = rowNum;
					digits[currentDigit].secondDigits[0].startOffset = rowNum;
					currentSecondDig = 0;
				}
				if (Math.floor(z.zip/1000)-currentDigit*10 > currentSecondDig) {
					digits[currentDigit].secondDigits[currentSecondDig].endOffset = rowNum;
					currentSecondDig = Math.floor(z.zip/1000)-currentDigit*10;
					digits[currentDigit].secondDigits[currentSecondDig].startOffset = rowNum;
				}
				if (z.state !== prevState) {
					if (digits[currentDigit].states.length > 0) {
						digits[currentDigit].states[digits[currentDigit].states.length-1].endOffset = rowNum;
					}
					digits[currentDigit].states.push({
						state:			z.state,
						startOffset:	rowNum,
						endOffset:		rowNum
					});
					prevState = z.state;
				}
			}

			digits[9].endOffset = zips.length;
			digits[9].secondDigits[9].endOffset = zips.length;
			digits[9].states[digits[9].states.length-1].endOffset = zips.length;

			// console.log(digits);
			// console.log(`${zips.length} ZIP codes`);

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
	});
</script>

<main>
	{#if zipCodes}
		<svg width={SVGWIDTH} height={SVGHEIGHT}>
			<ZIPScribble width={SVGWIDTH} height={SVGHEIGHT-60} {zipCodes}
				{zoomRange} {highlightRange} />
			<Navigator y={SVGHEIGHT-60} width={SVGWIDTH}
				{digits} numZIPs={zipCodes.length}
				bind:zoomRange={zoomRange} bind:highlightRange={highlightRange} />
		</svg>
	{/if}
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