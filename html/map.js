"use strict";

var mymap = L.map('mapid').setView([-22.9068467,-43.1728965], 3);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYXJ0dXJwaW1lbnRlbCIsImEiOiJjaXBnenJnYXUwMHcxdGRuamNjMnlicDhjIn0.5i67h6MPna8tfm__T8H8Mw', {
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
	maxZoom: 18,
	id: 'mapbox.streets',
	accessToken: 'pk.eyJ1IjoiYXJ0dXJwaW1lbnRlbCIsImEiOiJjaXBnenJnYXUwMHcxdGRuamNjMnlicDhjIn0.5i67h6MPna8tfm__T8H8Mw'
}).addTo(mymap);

var greenIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var xmlhttp = new XMLHttpRequest();
var url = "dengue_500tweets.csv";
var tweets;

xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
		tweets = Papa.parse(xmlhttp.responseText, {
			header: true,
			complete: function(results) {
				console.log(results);
			}
		});

		for (var i = tweets['data'].length - 1; i >= 0; i--) {
			var tweet = tweets['data'][i]
			var marker = L.marker([parseFloat(tweet['latitude']), parseFloat(tweet['longitude'])]).addTo(mymap);
			marker.bindPopup("<b>Text:</b> " + tweet['text'] + "<br><b>Language:</b> " + tweet['language'] + "<br><b>Date:</b> " + tweet['send_time'] + "<br><b>Location Type:</b> " + tweet['loc_type']);
		};
	}
};

//var greenMarker = L.marker([51.5, -0.09], {icon: greenIcon}).addTo(mymap);

xmlhttp.open("GET", url, true);
xmlhttp.send();

var xmlhttpZika = new XMLHttpRequest();
var urlZika = "zika_500tweets.csv";
var tweetsZika;

xmlhttpZika.onreadystatechange = function() {
	if (xmlhttpZika.readyState == 4 && xmlhttpZika.status == 200) {
		tweetsZika = Papa.parse(xmlhttpZika.responseText, {
			header: true,
			complete: function(results) {
				console.log(results);
			}
		});

		for (var i = tweetsZika['data'].length - 1; i >= 0; i--) {
			var tweet = tweetsZika['data'][i]
			var marker = L.marker([parseFloat(tweet['latitude']), parseFloat(tweet['longitude'])], {icon: greenIcon}).addTo(mymap);
			marker.bindPopup("<b>Text:</b> " + tweet['text'] + "<br><b>Language:</b> " + tweet['language'] + "<br><b>Date:</b> " + tweet['send_time'] + "<br><b>Location Type:</b> " + tweet['loc_type']);
		};
	}
};

xmlhttpZika.open("GET", urlZika, true);
xmlhttpZika.send();