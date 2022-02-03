<script>

	import { extent } from 'd3-array';
	import { interpolateZoom } from 'd3-interpolate';
	import { tweened } from 'svelte/motion';

	export let x = 0;
	export let y = 0;
	export let width;
	export let height;
	export let zipCodes;
	export let states;
	export let zoomRange;
	export let highlightRange;
	
	let view;
	let interpolator;
	const t = tweened(0);

	const prevAlpha = tweened(0);
	let prevPath = null;
	const currentAlpha = tweened(1);
	let currentPath = null;

	let fullPath = '';

	$: if (zipCodes && height > 0 && width > 0) {
		view = makeView(zipCodes);
		fullPath = makePath(zipCodes);
	}

	$: if (zoomRange) {
		subsetZIPs(zipCodes, zoomRange);
	}

	$: if (highlightRange) {
		if (highlightRange === []) {
			currentPath = fullPath;
		} else {
			currentPath = makePath(zipCodes.slice(highlightRange[0], highlightRange[1]));
		}
	}

	function makeView(zips) {
		const xExt = extent(zips, z => z.lon_proj);
		const yExt = extent(zips, z => z.lat_proj);
		const size = xExt[1]-xExt[0] > (yExt[1]-yExt[0]) * (width/height) ? (xExt[1]-xExt[0]) * (height/width) : yExt[1]-yExt[0];
		const newView = [(xExt[0]+xExt[1])/2, (yExt[0]+yExt[1])/2, size * 1.05];

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

		const k = height / v[2]; // scale
		const translate = [x + width / 2 - v[0] * k, y + height / 2 - v[1] * k]; // translate

		return `translate(${translate}) scale(${k})`;
	}
</script>

{#if zipCodes}
<g transform={makeTransform($t)}>
	{#each states as statePolys}
		{#each statePolys.geo as p}
			<path d={makePath(p)} class="state" />
		{/each}
	{/each}
	{#if zoomRange && zoomRange.length > 0}
		<path d={fullPath} class="background" />
	{/if}
	{#if prevPath && $prevAlpha > 0}
		<path d={prevPath} style={`opacity:${$prevAlpha};`} />
	{/if}
	<path d={currentPath} style={`opacity:${$currentAlpha};`} />
</g>
{/if}

<style>
	path {
		stroke: #333;
		stroke-width: .5px;
		stroke-linejoin: miter;
		fill: none;
	}

	path.background {
		stroke: #ccc;
	}

	path.state {
		stroke: white;
		fill: #eee;
	}

	@media (prefers-color-scheme: dark) {
		path {
			stroke: lightgray;
		}

		path.background {
			stroke: #666;
		}

		path.state {
			stroke: #333;
			stroke-width: 2px;
			fill: #444;
		}
	}
</style>