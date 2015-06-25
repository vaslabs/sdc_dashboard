var marker = null;
var minAlt, maxAlt;
var gpsEntries, altitudeEntries;
function startAnimating(data) {
  gpsEntries = data.gpsEntries;
  var lat = gpsEntries[0].latitude;
  var lng = gpsEntries[0].longitude;
  var myLatlng = new google.maps.LatLng(lat,lng);
  var mapOptions = {
    zoom: 16,
    center: myLatlng
  }

  if (marker == null) {
    marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: 'GPS data'
    });
    marker.setIcon("http://maps.google.com/mapfiles/ms/icons/red-dot.png");
  
  }
  
  altitudeEntries = data.barometerEntries;
  altitudeEntries = altitudeEntries.sort(function(entryA, entryB) {
    return entryA.timestamp - entryB.timestamp;
  });
  if (altitudeEntries.length > 0) {
    maxAlt = altitudeEntries[0].altitude;
    minAlt = altitudeEntries[0].altitude;
    $.each(altitudeEntries, function(key, alt) {
      if (alt.altitude > maxAlt) {
        maxAlt = alt.altitude;
      }
      if (alt.altitude < minAlt) {
        minAlt = alt.altitude;
      }
    });
    
  }
  animateEvents(gpsEntries, altitudeEntries);
 
}

function drawPath(data) {
  var flightPlanCoordinates = [];
  for (var i = 0; i < data.gpsEntries.length; i++) {
      flightPlanCoordinates.push(new google.maps.LatLng(data.gpsEntries[i].latitude, data.gpsEntries[i].longitude));
  }
  var flightPath = new google.maps.Polyline({
  path: flightPlanCoordinates,
  geodesic: true,
  strokeColor: '#FF0000',
  strokeOpacity: 1.0,
  strokeWeight: 2
  });

  flightPath.setMap(map);
}

var speed = 100;

function barometerEvent(altitude) {
  var percentage = (altitude - minAlt)/(maxAlt - minAlt);
  var progress = Math.round(percentage*100);
  $('#current-altitude').text(altitude);
  $('#progress_bar').data('progress', percentage);
  $('#progress_bar').height(progress + "%");
}

function gpsEvent(longitude, latitude) {
  var lat = data.gpsEntries[i].latitude;
  var lng = data.gpsEntries[i].longitude;
  var position = new google.maps.LatLng(lat, lng);

  marker.setPosition(position);
  map.panTo(position);     

}



function animateEvents(gpsEntries, altitudeEntries) {
  
  var debugGPS = function (lat, lng) {
    console.log("gps : " + lat + "," + lng);
  }
  var debugAlt = function (alt) {
    console.log("alt: " + alt);
  }

  var serialisedEvents = serialiseEvents(gpsEntries, altitudeEntries, gpsEvent, barometerEvent);
  var previousTimestamp = serialisedEvents[0].timestamp;
  for (var i = 0; i < serialisedEvents.length; i++) {
    var delay = (serialisedEvents[i].timestamp - previousTimestamp)/speed;
    previousTimestamp = serialisedEvents[i];
    setTimeout(serialisedEvents.eventCall(), delay);
  }//for

}