var map = L.map('map').setView([28.028533732226855, 85.08676171302795], 14);

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
    maxZoom: 18
});//.addTo(map);

var OpenStreetMap_DE = L.tileLayer('http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

 markerClusterLayer = L.markerClusterGroup({
    disableClusteringAtZoom: 13
  });//.addTo(map);

var items = [];

// nice leaflet-ajax plugin
// https://github.com/calvinmetcalf/leaflet-ajax
var geojsonLayer = L.geoJson.ajax('salme_baseline.geojson', {
  onEachFeature: function(data, layer) {
    items.push(layer); 
  //  layer.bindPopup('<h3>' + data.properties.general_info_registration_number + '</h3>');
	layer.bindPopup("<h5>Household Info</h5><hr>"
						+"<b><font color='#e74c3c'>Registration number:</font></b> " + data.properties.general_info_registration_number
						+ "<br>" 
						+ "<b><font color='#2c3e50'>Owner name:</font></b>  " + data.properties.govt_hoh_name
						+"<br>"
						+ "<b><font color='#3498db'>Ward:</font></b>  " + data.properties.general_info_ward
						+ "<br>" 
						+ "<b><font color='#1abc9c'>Tole:</font></b>  " + data.properties.general_info_tole
						+ "<hr>" 
						+ "<b><font color='#e74c3c'>Damage Type:</font></b>  " + data.properties.house_info_dam_type
						+ "<br>" 
						+ "<b><font color='##2c3e50'>Residing Location:</font></b>  " + data.properties.house_info_residing_loc+"<hr>"
					//	+ "<b><font color='#1abc9c'>Tole:</font></b>  " + data.properties.general_info_tole);
					//	+ "<img src='http://52.204.31.159/omk/data/submissions/baseline_reconstruction/15c7dd7f-70da-4666-83c1-a8a412267c75/"+data.properties.image_house+"' alt=\"blue box\" height=\"10\" width=\"10\">" );
						+ "<img src='../imgs/submissions/baseline_reconstruction/"+(data.properties.meta_instanceId).slice(5)+"/"+data.properties.image_house+"' alt=\"./oth.jpg\" onerror=\"this.onerror=null;this.src='js/ff.jpg';\" height=\"200\" width=\"200\">" );
  }
});
//marker1.bindPopup( "<img src=" + icon_url + "/> Current temperature in " + location + " is: " + temp_f)
//<img src="09fg05-blue-box.gif" alt="blue box" height="10" width="10">




geojsonLayer.addTo(map);
  
L.control.search({
  data: items
}).addTo(map);
/*
//adding custom files to the map
var style = {color:'red', opacity: 1.0, fillOpacity: 1.0, weight: 2, clickable: false};
		L.Control.FileLayerLoad.LABEL = '<i class="fa fa-folder-open"></i>';
		L.Control.fileLayerLoad({
			fitBounds: true,
			layerOptions: {style: style,
						   pointToLayer: function (data, latlng) {
							  return L.circleMarker(latlng, {style: style});
						   }},
		}).addTo(map);
*/		