<script>

	import { scaleLinear } from "d3-scale";
	import { onMount } from 'svelte';

	export let x = 0;
	export let y;
	export let width;
	export let height;
	export let digits;
	export let states;
	export let numZIPs;
	export let range = [];

	let xScale = scaleLinear([0, numZIPs], [1, width]);

	let activeDigit = -1;
	let activeState = -1;

	let svg;
	let point;

	onMount(() => {
		svg = document.querySelector('svg');
		point = svg.createSVGPoint();
	});

	function mouseMove(e) {
		point.x = e.clientX;
		point.y = e.clientY;
		point = point.matrixTransform(svg.getScreenCTM().inverse());

		// console.log(point.x, point.y-y);
		if (point.y-y <= 20) {
			let digit = 9;
			while (point.x < xScale(digits[digit])) {
				digit -= 1;
			}
			if (digit != activeDigit) {
				if (digit < 9)
					range = [digits[digit], digits[digit+1]];
				else
					range = [digits[digit], numZIPs];

				activeDigit = digit;
			}
		} else if (point.y-y >= 30) {
			let mouseOffset = xScale.invert(point.x);
			let state = states.length-1;
			while (states[state].offset > mouseOffset) {
				state -= 1;
			}
			if (state !== activeState) {
				if (state < states.length-1)
					range = [states[state].offset, states[state+1].offset];
				else
					range = [states[state].offset, numZIPs];
				activeState = state;
			}
		} else {
			activeDigit = -1;
			activeState = -1;
		}
	}

	function mouseLeave() {
		range = [];
		activeDigit = -1;
		activeState = -1;
	}

	function mouseClick() {

	}

</script>

<g transform={`translate(${x}, ${y})`}>
	<rect x={0} y={0} {width} {height} class="background"
		on:mousemove={mouseMove} on:mouseleave={mouseLeave}
		on:click={mouseClick} />
	<rect x={0} y={height-30} width={width} height={10} class="bar" />
	{#each digits as d, i}
		{#if i === activeDigit}
			<rect x={xScale(digits[i])} y={0} width={i < 9 ? xScale(digits[i+1])-xScale(digits[i]) : width-xScale(digits[i])} height={20} class="active" />
		{/if}
		<line x1={xScale(d)} y1={0} x2={xScale(d)} y2={height-30} />
		<text x={i < 9 ? (xScale(d)+xScale(digits[i+1]))/2 : (xScale(d)+width)/2 } y={height-37} >{i}</text>
	{/each}
	{#each states as state, i}
		{#if activeState === i || (activeState >= 0 && states[activeState].state === states[i].state) }
			<rect x={xScale(states[i].offset)} y={30} width={i < states.length-1 ? xScale(states[i+1].offset)-xScale(states[i].offset) : width-xScale(states[i].offset)} height={20} class="active" />
		{/if}
		<line x1={xScale(state.offset)} y1={height-20} x2={xScale(state.offset)} y2={height} />
		{#if i < states.length-1 && xScale(states[i+1].offset)-xScale(state.offset) > 20}
			<text x={i < states.length-1 ? (xScale(state.offset)+xScale(states[i+1].offset))/2 : (xScale(state.offset)+width)/2 } y={height-5} >{state.state}</text>
		{/if}
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

	rect.active {
		fill: lightsteelblue;
		pointer-events: none;
	}

	rect.background {
		fill: white;
		pointer-events: all;
	}
</style>