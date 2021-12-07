<script>

	import { scaleLinear } from 'd3-scale';
	import { extent } from 'd3-array';

	export let x = 0;
	export let y = 0;
	export let width;
	export let height;
	export let zipCodes;
	export let range;

	let xScale;
	let yScale;

	$: if (zipCodes) {
		xScale = scaleLinear(extent(zipCodes, z => z.lon_proj), [0, width]);
		yScale = scaleLinear(extent(zipCodes, z => z.lat_proj), [0, height]);
	}

	function subsetZIPs(zips, range) {
		if (range && range.length > 0) {
			return zips.filter(z => z.zip >= range[0] && z.zip <= range[1]);
		} else {
			return zips;
		}
	}

	function makePath(zips) {		
		return 'M '+zips.map(z => `${xScale(z.lon_proj)},${yScale(z.lat_proj)}`).join(' L ');
	}
</script>

{#if zipCodes}
<g transform={`translate(${x}, ${y})`}>
	{#if range && range.length > 0}
		<path d={makePath(zipCodes)} class="background" />
	{/if}
	<path d={makePath(subsetZIPs(zipCodes, range))} />
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