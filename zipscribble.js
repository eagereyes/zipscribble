/*
	Copyright (c) 2012, Robert Kosara <rkosara@me.com>
	
	Permission to use, copy, modify, and/or distribute this software for any
	purpose with or without fee is hereby granted, provided that the above
	copyright notice and this permission notice appear in all copies.
	
	THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
	WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
	MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
	ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
	WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
	ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
	OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/

var map;

var mapLayer;

var scribbleLayer;

var boundingboxes;

function makeGeoJSONURL(country) {
	return 'data/zipscribble_'+country+'.json';
}

function initMap(){

	$.getJSON('data/boundingboxes.json', function(bb) {
		boundingboxes = bb;
	});

	var po = org.polymaps;
	
	map = po.map()
	    .container(document.getElementById("map").appendChild(po.svg("svg")))
	    .add(po.interact())
	    .add(po.hash());
	
	mapLayer = po.image()
	    .url(po.url("http://{S}tile.cloudmade.com"
	    + "/b12a0bb2f7844dda8b214fda256a6bbd" // please get your own API key if you use this somewhere else!
	    + "/998/256/{Z}/{X}/{Y}.png")
	    .hosts(["a.", "b.", "c.", ""]));
	
	map.add(mapLayer);
	
	scribbleLayer = po.geoJson().url(makeGeoJSONURL('US'));
	
	map.add(scribbleLayer);
	
	map.add(po.compass()
	    .pan("none"));
}

function toggleMap(mapOn) {
	mapLayer.visible(mapOn);
}

function switchCountry(selector) {
	var country = selector.value;
	scribbleLayer.url(makeGeoJSONURL(country));
	map.extent(boundingboxes[country]);
}
