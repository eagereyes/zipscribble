<script>

	import { scaleLinear } from 'd3-scale';
	import { extent } from 'd3-array';

	export let x = 0;
	export let y = 0;
	export let width;
	export let height;
	export let zipCodes;
	export let range;
	export let view;

	let xScale;
	let yScale;

	let maxView;
	let scaleWidth = true;

	$: if (zipCodes) {
		xScale = scaleLinear(extent(zipCodes, z => z.lon_proj), [-width/2, width/2]);
		yScale = scaleLinear(extent(zipCodes, z => z.lat_proj), [-height/2, height/2]);
		// xScale = scaleLinear(extent(zipCodes, z => z.lon_proj), [0, width]);
		// yScale = scaleLinear(extent(zipCodes, z => z.lat_proj), [0, height]);
		view = maxView = makeView(zipCodes);
	}

	function makeView(zips) {
		const xExt = extent(zips, z => xScale(z.lon_proj));
		const yExt = extent(zips, z => yScale(z.lat_proj));
		scaleWidth = xExt[1]-xExt[0] > yExt[1]-yExt[0];
		return [(xExt[1]+xExt[1])/2, (yExt[0]+yExt[1])/2, (scaleWidth ? xExt[1]-xExt[0] : yExt[1]-yExt[0]) * 1.05];
	}

	function subsetZIPs(zips, range) {
		if (range && range.length > 0) {
			const z = zips.slice(range[0], range[1]);
			view = makeView(z);
			return z;
		} else {
			view = maxView;
			scaleWidth = true;
			return zips;
		}
	}

	function makePath(zips) {		
		return 'M '+zips.map(z => `${xScale(z.lon_proj)},${yScale(z.lat_proj)}`).join(' L ');
	}

	// https://observablehq.com/@d3/d3-interpolatezoom
	function makeTransform(t) {
		// const view = interpolator(t);

		const k = (scaleWidth ? width : height) / view[2]; // scale
		const translate = [width / 2 - view[0] * k, height / 2 - view[1] * k]; // translate

		return `translate(${translate}) scale(${k})`;
	}
</script>

{#if zipCodes}
<!-- <g transform={`translate(${x}, ${y})`}> -->
<g transform={`translate(${width/2}, 0)`}>
<g transform={makeTransform(view)}>
	{#if range && range.length > 0}
		<path d={makePath(zipCodes)} class="background" />
	{/if}
	<path d={makePath(subsetZIPs(zipCodes, range))} />
</g>
</g>
{/if}

<style>
	path {
		stroke: #333;
		stroke-width: 1px;
		fill: none;
	}

	path.background {
		stroke: lightgrey;
	}
</style>