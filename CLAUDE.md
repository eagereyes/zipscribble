# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev        # Start dev server (Vite)
npm run build      # Production build
npm run preview    # Preview production build
npm run check      # Type-check with svelte-check
```

Data processing (run from repo root):
```bash
bin/download.sh           # Download ZIP code data from geonames (touch target files first)
python3 bin/txt2json.py   # Convert .txt data files → GeoJSON + countryinfo.json
```

## Architecture

This is a **Svelte 5 + SvelteKit + Vite** app. The UI is entirely SVG-based — there is no HTML canvas or map library.

### Frontend (`src/`)

- **`routes/+page.svelte`** — SvelteKit entry point; simply renders `<App />`.

- **`App.svelte`** — Root component. Loads `static/data/us-lower48.csv` (ZIP codes) and `static/data/us-states-20m.json` (state boundaries) on mount. Applies `d3-geo` Albers projection to all coordinates. Builds a `digits` data structure indexing ZIPs by first digit (0–9), second digit (0–9), and state, with start/end offsets into the sorted ZIP array.

- **`ZIPScribble.svelte`** — Renders the map as SVG `<path>` elements. Uses `d3-interpolate`'s `interpolateZoom` and Svelte `tweened` stores for animated zoom transitions when the selection changes. The scribble line is a single SVG polyline path through all ZIP coordinates in numeric order. Three `$effect` blocks (zipCodes/dimensions, zoomRange, highlightRange) each use `untrack()` internally to prevent reactive cycles — this pattern is load-bearing, don't remove it.

- **`Navigator.svelte`** — The horizontal bar UI at the bottom. Three rows of clickable/hoverable `<rect>` elements representing first digit, second digit, and state breakdown. Keyboard navigation (digit keys, arrow keys) drives `zoomRange` and `highlightRange` back up to `App.svelte`.

- **`Title.svelte`** — Displays the current ZIP range and place names.

### Data Pipeline (`bin/` → `data/`)

- Source data: tab-separated `.txt` files from [geonames](http://download.geonames.org/export/zip/) in `data/`
- `bin/txt2json.py` converts them to `data/zipscribble_XX.json` (GeoJSON LineString or FeatureCollection) and `data/countryinfo.json` (bounding boxes per country)
- The US-specific visualization uses `static/data/us-lower48.csv` (from Simple Maps), not the geonames JSON files; static assets are served from `static/` (SvelteKit convention)

### Data flow

ZIP CSV → `App.svelte` projects coordinates → builds `digits` index → `Navigator` sets `zoomRange`/`highlightRange` → `ZIPScribble` slices the ZIP array and zooms/highlights the path.
