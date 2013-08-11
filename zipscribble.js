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

var countryInfo;

var currentCountry = 'US';

var showStates = false;

var PATH;

var stateColors = {}

function makeGeoJSONURL(country) {
	return PATH+'zipscribble_'+country+'.json';
}

function setCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) {
        	return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}

function initMap(){

	if (document.location.hostname == "")
		PATH = 'data/';
	else
		PATH = '/media/zipscribble/data/';

	jQuery.ajax({
		url: PATH+'countryinfo.json',
		async: false,
		dataType: 'json',
		success: function (info) {
			countryInfo = info;
		}
	});

	var po = org.polymaps;
	
	var svg = po.svg('svg');
	svg.setAttribute('width', '100%');
	svg.setAttribute('height', '100%');

	map = po.map()
	    .container(document.getElementById("map").appendChild(svg))
	    .add(po.interact());
	
	mapLayer = po.image()
	    .url(po.url("http://{S}tile.cloudmade.com"
	    + "/b12a0bb2f7844dda8b214fda256a6bbd" // please get your own API key if you use this somewhere else!
	    + "/998/256/{Z}/{X}/{Y}.png")
	    .hosts(["a.", "b.", "c.", ""]));
	
	map.add(mapLayer);
	
	scribbleLayer = po.geoJson();
	
	map.add(scribbleLayer.on('load', po.stylist()
		.attr('stroke', function(d) {
			if (showStates) {
				if (d.id == '000stateconnectors')
					return 'gray'
				else {
					if (stateColors[d.id] === undefined) {
						stateColors[d.id] = 'rgb('+Math.floor(Math.random()*160)+','+Math.floor(Math.random()*160)+','+Math.floor(Math.random()*160)+')';
					}
					return stateColors[d.id];
				}
			} else {
				return 'black';
			}
	})));
	
	map.add(po.compass()
	    .pan("none"));

	if (document.location.hash.length == 0)
		switchCountry(getCookie('lastCountry') || 'US', true);

	map.add(po.hash().parser(hash_parser).formatter(hash_formatter));
}

function toggleMap(mapOn) {
	mapLayer.visible(mapOn);
}

function toggleStates(statesOn) {
	showStates = statesOn;
	scribbleLayer.reload();
	stateColors = {};
}

function switchCountry(country, panMap) {
	currentCountry = country;
	jQuery('#country')[0].value = country;
	scribbleLayer.url(makeGeoJSONURL(country));
	setCookie('lastCountry', country, 30);
	if (panMap) {
//		console.log(countryInfo[country].bbox);
		map.extent(countryInfo[country].bbox);
	}
	if (countryInfo[country].states) {
		jQuery('#showStates').removeAttr('disabled');
		showStates = jQuery('#showStates')[0].checked;
	} else {
		jQuery('#showStates').attr('disabled', 'disabled');
		showStates = false;
	}
	stateColors = {};
}

// hash functions slightly modified from https://github.com/simplegeo/polymaps/pull/41
function hash_parser(map, s) {
	var args = s.split("/");
	var coords = args.slice(1, 4).map(Number);
	if (countryInfo[args[0]] != undefined)
		switchCountry(args[0], coords.length == 0);
	else
		return true;
	if (coords.length == 3 && !coords.some(isNaN)) {
		var lat = 90 - 1e-8;
		var size = map.size();
		map.zoomBy(coords[0] - map.zoom(),
			{x: size.x / 2, y: size.y / 2},
			{lat: Math.min(lat, Math.max(-lat, coords[1])), lon: coords[2]});
	}
}

function hash_formatter(map) {
  var center = map.center(),
      zoom = map.zoom(),
      precision = Math.max(0, Math.ceil(Math.log(zoom) / Math.LN2));
  return "#" + currentCountry
      + "/" + zoom.toFixed(2)
      + "/" + center.lat.toFixed(precision)
      + "/" + center.lon.toFixed(precision)
      ;
}

initMap();
