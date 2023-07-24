<script>

	import { scaleLog } from 'd3-scale';
	import { extent } from 'd3-array';

	export let x = 0;
	export let y = 0;
	export let width;
	export let height;
	export let places;

	let barWidth;
	let yScale;

	let activeIndex = -1;
	export let range = [];

	$: if (places) {
		yScale = scaleLog(extent(places, p => p.zips), [0, height]);
		barWidth = Math.floor(width/places.length);
	}

	function mouseMove(e) {
		activeIndex = Math.floor(e.offsetX/barWidth);
		range = [places[activeIndex].firstZIP, places[activeIndex].firstZIP+places[activeIndex].zips];
	}

	function mouseLeave() {
		activeIndex = -1;
		range = [];
	}

	function mouseClick() {

	}

</script>

<g transform={`translate(${x},${y})`}>
	<rect x={0} y={0} {width} {height} class="overlay"
		on:mouseleave={mouseLeave}
		on:mousemove={mouseMove} on:mousedown={mouseClick} />
	{#each places as p, i}
		<rect x={i*barWidth} y={height-yScale(p.zips)} width={barWidth-1} height={yScale(p.zips)} class={activeIndex === i ? 'active' : 'zipbar'} />
	{/each}
	{#if activeIndex >= 0}
		<text x={0} y={height}>{`${places[activeIndex].name}: ${places[activeIndex].firstZIP}-${places[activeIndex].firstZIP+places[activeIndex].zips}`}</text>
	{/if}
</g>

<style>
	rect.overlay {
		fill: none;
		pointer-events: all;
	}

	rect.active {
		fill: steelblue;
		pointer-events: none;
	}

	.zipbar {
		fill: lightgray;
		pointer-events: none;
	}
</style>