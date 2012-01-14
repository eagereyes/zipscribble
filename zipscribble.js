
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
	    + "/b12a0bb2f7844dda8b214fda256a6bbd"
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
