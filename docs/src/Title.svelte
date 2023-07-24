<script>

    export let width;
    export let height;
    export let title;
    export let subtitle;

</script>

<rect x={0} y={0} {width} {height} />
<text x={5} y={20}>{title}</text>
<text x={5} y={40}>{subtitle}</text>

<style>
    text {
        fill: white;
    }
</style>