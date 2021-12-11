<script>

	import { extent } from 'd3-array';
	import { interpolateZoom } from 'd3-interpolate';
	import { tweened } from 'svelte/motion';

	export let x = 0;
	export let y = 0;
	export let width;
	export let height;
	export let zipCodes;
	export let range;
	export let view;

	let scaleWidth = true;
	let interpolator;
	const t = tweened(0);

	const prevAlpha = tweened(0);
	let prevPath = null;
	const currentAlpha = tweened(1);
	let currentPath = null;

	$: if (zipCodes) {
		view = makeView(zipCodes);
	}

	$: if (range) {
		subsetZIPs(zipCodes, range);
	}

	function makeView(zips) {
		const xExt = extent(zips, z => z.lon_proj);
		const yExt = extent(zips, z => z.lat_proj);
		scaleWidth = xExt[1]-xExt[0] > (yExt[1]-yExt[0]) * (width/height);
		const newView = [(xExt[0]+xExt[1])/2, (yExt[0]+yExt[1])/2, (scaleWidth ? xExt[1]-xExt[0] : yExt[1]-yExt[0]) * 1.05];

		if (view) {
			interpolator = interpolateZoom(view, newView);
			t.set(0, {duration: 0});
			t.set(1, {duration: interpolator.duration/2});
		}

		prevPath = currentPath;
		prevAlpha.set(1, {duration: 0});
		prevAlpha.set(0, {duration: interpolator ? interpolator.duration/2 : 200});
		currentPath = makePath(zips);
		currentAlpha.set(0, {duration: 0});
		currentAlpha.set(1, {duration: interpolator ? interpolator.duration/2 : 200});

		return newView;
	}

	function subsetZIPs(zips, range) {
		if (range && range.length > 0) {
			const z = zips.slice(range[0], range[1]);
			view = makeView(z);
			return z;
		} else {
			view = makeView(zips);
			return zips;
		}
	}

	function makePath(zips) {	
		return 'M '+zips.map(z => `${z.lon_proj},${z.lat_proj}`).join(' L ');
	}

	// https://observablehq.com/@d3/d3-interpolatezoom
	function makeTransform(t) {
		const v = interpolator ? interpolator(t) : view;

		const k = (scaleWidth ? width : height) / v[2]; // scale
		const translate = [x + width / 2 - v[0] * k, y + height / 2 - v[1] * k]; // translate

		return `translate(${translate}) scale(${k})`;
	}
</script>

{#if zipCodes}
<!-- <g transform={`translate(${x}, ${y})`}> -->
<g transform={makeTransform($t)}>
	{#if range && range.length > 0}
		<path d={makePath(zipCodes)} class="background" />
	{/if}
	{#if prevPath && $prevAlpha > 0}
		<path d={prevPath} style={`stroke:rgba(51,51,51,${$prevAlpha});`} />
	{/if}
	<!-- <path d={makePath(subsetZIPs(zipCodes, range))} /> -->
	<path d={currentPath} style={`stroke:rgba(51,51,51,${$currentAlpha});`} />
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