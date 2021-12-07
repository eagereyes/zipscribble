<script>

	import { scaleLinear } from "d3-scale";

	export let x = 0;
	export let y;
	export let width;
	export let height;
	export let digits;
	export let states;
	export let numZIPs;
	export let range = [];

	let xScale = scaleLinear([0, numZIPs], [0, width]);

	let prevDigit = -1;

	function mouseMove(e) {
		console.log(e.clientX);
		let digit = 9;
		while (e.clientX < xScale(digits[digit])) {
			digit -= 1;
		}
		if (digit != prevDigit) {
			if (digit < 9)
				range = [digits[digit], digits[digit+1]];
			else
				range = [digits[digit], numZIPs];

			prevDigit = digit;
		}
	}

	function mouseLeave() {
		range = [];
		prevDigit = -1;
	}

</script>

<g transform={`translate(${x}, ${y})`}>
	<rect x={0} y={0} {width} {height} class="background"
		on:mousemove={mouseMove} on:mouseleave={mouseLeave} />
	<rect x={0} y={height-40} width={width} height={20} class="bar" />
	{#each digits as d, i}
		<line x1={xScale(d)} y1={0} x2={xScale(d)} y2={height-40} />
		<text x={i < 9 ? (xScale(d)+xScale(digits[i+1]))/2 : (xScale(d)+width)/2 } y={height-42} >{i}</text>
	{/each}
	{#each states as state, i}
		<line x1={xScale(state.offset)} y1={height-20} x2={xScale(state.offset)} y2={height} />
		<text x={i < states.length-1 ? (xScale(state.offset)+xScale(states[i+1].offset))/2 : (xScale(state.offset)+width)/2 } y={height-5} >{state.state}</text>
	{/each}
</g>

<style>
	rect.bar {
		fill: lightgray;
		stroke: none;
		pointer-events: none;
	}

	line {
		stroke: darkgray;
		pointer-events: none;
	}

	text {
		fill: darkgray;
		font-size: 8pt;
		text-anchor: middle;
		pointer-events: none;
	}

	rect.background {
		fill: white;
		pointer-events: all;
	}
</style>