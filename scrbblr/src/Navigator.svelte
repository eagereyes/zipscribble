<script>

	import { scaleLinear } from "d3-scale";
	import { onMount } from 'svelte';

	export let x = 0;
	export let y;
	export let width;
	export let height;
	export let digits;
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
		let digit = 9;
		while (point.x < xScale(digits[digit].lastIndex)) {
			digit -= 1;
		}
		if (digit != activeDigit) {
			if (digit < 9)
				range = [digits[digit].lastIndex, digits[digit+1].lastIndex];
			else
				range = [digits[digit].lastIndex, numZIPs];

			activeDigit = digit;
		}

		let mouseOffset = xScale.invert(point.x);
		const states = digits[activeDigit].states;
		let state = states.length-1;
		while (states[state].startOffset > mouseOffset) {
			state -= 1;
		}
		if (state !== activeState) {
			// if (state < states.length-1)
			// 	range = [states[state].offset, states[state+1].offset];
			// else
			// 	range = [states[state].offset, numZIPs];
			// console.log(state);
			activeState = state;
		}

		if (y > 20 && y < 40) {
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
			<rect x={xScale(digits[i].lastIndex)} y={0} width={i < 9 ? xScale(digits[i+1].lastIndex)-xScale(digits[i].lastIndex) : width-xScale(digits[i].lastIndex)} height={20} class="active" />
		{/if}
		<line x1={xScale(d.lastIndex)} y1={0} x2={xScale(d.lastIndex)} y2={height-30} />
		<text x={i < 9 ? (xScale(d.lastIndex)+xScale(digits[i+1].lastIndex))/2 : (xScale(d.lastIndex)+width)/2 } y={height-37} >{i}</text>
		{#each d.states as state, s}
			{#if (activeState === s && i === activeDigit) || ((activeState >= 0 && activeState < d.states.length && digits[activeDigit].states[activeState].state === d.states[s].state)) }
				<rect x={xScale(state.startOffset)} y={30} width={xScale(state.endOffset)-xScale(state.startOffset)} height={20} class="active" />
			{/if}
			<line x1={xScale(state.startOffset)} y1={height-20} x2={xScale(state.startOffset)} y2={height} />
			{#if xScale(state.endOffset)-xScale(state.startOffset) > 20}
				<text x={(xScale(state.startOffset)+xScale(state.endOffset))/2} y={height-5} >{state.state}</text>
			{/if}
		{/each}
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