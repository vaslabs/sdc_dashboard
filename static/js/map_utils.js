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
  prepareEvents(gpsEntries, altitudeEntries);
 
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
var serialisedEvents;
function barometerEvent(eventIndex) {
  var altitude = serialisedEvents[eventIndex].altitude;
  var percentage = (altitude - minAlt)/(maxAlt - minAlt);
  var progress = Math.round(percentage*100);
  $('#current-altitude').text(altitude);
  $('#progress_bar').data('progress', percentage);
  $('#progress_bar').height(progress + "%");
  nextEvent(eventIndex);
}

function gpsEvent(eventIndex) {
  var lat = serialisedEvents[eventIndex].latitude;
  var lng = serialisedEvents[eventIndex].longitude;
  var position = new google.maps.LatLng(lat, lng);

  marker.setPosition(position);
  map.panTo(position);     
  nextEvent(eventIndex);
}

function nextEvent(eventIndex) {
  var previousTimestamp = serialisedEvents[eventIndex].timestamp;
  eventIndex += 1;
  if (eventIndex >= serialisedEvents.length)
      return;
  var nextTimestamp = serialisedEvents[eventIndex].timestamp;
  var timeDiff = (nextTimestamp - previousTimestamp)/speed;
  if (serialisedEvents[eventIndex].event_type == "barometer") {
      setTimeout(function() {barometerEvent(eventIndex);}, timeDiff);
  } else if (serialisedEvents[eventIndex].event_type == "gps") {
      setTimeout(function() {gpsEvent(eventIndex);}, timeDiff);
  }
}//nextEvent

function prepareEvents(gpsEntries, altitudeEntries) {
  
  
  serialisedEvents = serialiseEvents(gpsEntries, altitudeEntries);
  var previousTimestamp = serialisedEvents[0].timestamp;
  
  
  if (serialisedEvents[0].event_type == "barometer") {
    barometerEvent(0);
  } else if (serialisedEvents[0].event_type == "gps") {
    gpsEvent(0);
  }

}