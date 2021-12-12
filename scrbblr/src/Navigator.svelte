<script>

	import { scaleLinear } from "d3-scale";
	import { onMount } from 'svelte';

	export let x = 0;
	export let y;
	export let width;
	export let digits;
	export let numZIPs;
	export let zoomRange = [];
	export let highlightRange = [];

	let xScale = scaleLinear([0, numZIPs], [1, width]);

	let activeFirst = -1;
	let activeSecond = -1;
	let activeState = -1;

	let timeoutID = 0;

	let svg;
	let point;

	onMount(() => {
		svg = document.querySelector('svg');
		point = svg.createSVGPoint();
	});

	function setActiveDigit(first, second, state) {
		if (timeoutID) {
			clearTimeout(timeoutID);
			timeoutID = 0;
		}
		if (first >= 0) {
			if (first !== activeFirst) {
				zoomRange = [digits[first].startOffset, digits[first].endOffset];
			}
			if (second >= 0) {
				highlightRange = [digits[first].secondDigits[second].startOffset, digits[first].secondDigits[second].endOffset];
			} else {
				highlightRange = zoomRange;
			}
		} else {
			timeoutID = setTimeout(() => {
				zoomRange = [];
				highlightRange = [];
				timeoutID = 0;
			}, 10);
		}
		activeFirst = first;
		activeSecond = second;
	}


</script>

<g transform={`translate(${x}, ${y})`}>
	{#each digits as d, i}
		<rect x={xScale(d.startOffset)} y={0} width={xScale(d.endOffset)-xScale(d.startOffset)} height={20}
			class={activeFirst === i ? 'active' : 'bar'}
			on:mouseenter={() => setActiveDigit(i)} on:mouseleave={() => setActiveDigit(-1)} />
		<line x1={xScale(d.startOffset)} y1={0} x2={xScale(d.startOffset)} y2={20} />
		<text x={(xScale(d.startOffset)+xScale(d.endOffset))/2} y={13} >{i}</text>
		{#each d.secondDigits as second, s}
			<rect x={xScale(second.startOffset)} y={20} width={xScale(second.endOffset)-xScale(second.startOffset)} height={20}
				class={activeFirst === i && activeSecond === s ? 'active' : 'bar'}
				on:mouseenter={() => setActiveDigit(i, s)} on:mouseleave={() => setActiveDigit(i, -1)} />
			<line x1={xScale(second.startOffset)} y1={20} x2={xScale(second.startOffset)} y2={40} />
		{/each}
		{#each d.states as state, s}
			<rect x={xScale(state.startOffset)} y={40} width={xScale(state.endOffset)-xScale(state.startOffset)} height={20} class={activeState === state ? 'active' : 'bar'} />
			<line x1={xScale(state.startOffset)} y1={40} x2={xScale(state.startOffset)} y2={60} />
			{#if xScale(state.endOffset)-xScale(state.startOffset) > 20}
				<text x={(xScale(state.startOffset)+xScale(state.endOffset))/2} y={55} >{state.state}</text>
			{/if}
		{/each}
		<line x1={0} y1={20} x2={width} y2={20} />
		<line x1={0} y1={40} x2={width} y2={40} />
		<line x1={width-0.5} y1={0} x2={width-0.5} y2={60} />
	{/each}
</g>

<style>
	rect.bar {
		fill: white;
		stroke: none;
	}

	line {
		stroke: lightgray;
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
	}

	@media (prefers-color-scheme: dark) {
		rect.bar {
			fill: #222;
		}

		line {
			stroke: #444;
		}
	}
</style>