<script>

	import { scaleLinear } from 'd3-scale';
	import { extent } from 'd3-array';

	export let x = 0;
	export let y = 0;
	export let width;
	export let height;
	export let zipCodes;

	let xScale;
	let yScale;

	$: if (zipCodes) {
		xScale = scaleLinear(extent(zipCodes, z => z.lon_proj), [0, width]);
		yScale = scaleLinear(extent(zipCodes, z => z.lat_proj), [0, height]);
	}

	function makePath(zips) {
		return 'M '+zips.map(z => `${xScale(z.lon_proj)},${yScale(z.lat_proj)}`).join(' L ');
	}
</script>

{#if zipCodes}
<g transform={`translate(${x}, ${y})`}>
	<path d={makePath(zipCodes)} />
</g>
{/if}

<style>
	path {
		stroke: #333;
		stroke-width: 1px;
		fill: none;
	}
</style>