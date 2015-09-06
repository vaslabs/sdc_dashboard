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
        title: 'GPS data',
        icon: { path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW, scale: 1}
    });
  
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
  var gpsEntries = data.gpsEntries;
  var altitudeEntries = data.barometerEntries;
  altitudeEntries = averageBarometerValues(altitudeEntries, 1000);
  var skyDivingEvents = null;
  if (altitudeEntries.length > 0)
    skyDivingEvents = identifyFlyingEvents(altitudeEntries);

  //walking
  var flightPlanCoordinates = [];
  var wasLeftAt = 0;
  for (var i = 0; i < gpsEntries.length; i++) {
      if (skyDivingEvents != null && skyDivingEvents.takeoff.timestamp < gpsEntries[i].timestamp) {
        wasLeftAt = i;
        break;
      }
      flightPlanCoordinates.push(new google.maps.LatLng(gpsEntries[i].latitude, gpsEntries[i].longitude));
  }

  var flightPath = new google.maps.Polyline({
  path: flightPlanCoordinates,
  geodesic: true,
  strokeColor: '#000000',
  strokeOpacity: 1.0,
  strokeWeight: 2
  });

  flightPath.setMap(map);
  if (skyDivingEvents == null)
    return;
  //airplane
  flightPlanCoordinates = [];
  for (var i = wasLeftAt; i < gpsEntries.length; i++) {
      if (skyDivingEvents.freefall.timestamp < gpsEntries[i].timestamp) {
        wasLeftAt = i;
        break;
      }
      flightPlanCoordinates.push(new google.maps.LatLng(gpsEntries[i].latitude, gpsEntries[i].longitude));
  }
  flightPath = new google.maps.Polyline({
  path: flightPlanCoordinates,
  geodesic: true,
  strokeColor: '#0000FF',
  strokeOpacity: 1.0,
  strokeWeight: 2
  });

  flightPath.setMap(map);

  //Free fall
  flightPlanCoordinates = [];
  for (var i = wasLeftAt; i < gpsEntries.length; i++) {
      if (skyDivingEvents.canopy.timestamp < gpsEntries[i].timestamp) {
        wasLeftAt = i;
        break;
      }
      flightPlanCoordinates.push(new google.maps.LatLng(gpsEntries[i].latitude, gpsEntries[i].longitude));
  }
  flightPath = new google.maps.Polyline({
  path: flightPlanCoordinates,
  geodesic: true,
  strokeColor: '#FF0000',
  strokeOpacity: 1.0,
  strokeWeight: 2
  });

  flightPath.setMap(map);

  //Canopy
  flightPlanCoordinates = [];
  for (var i = wasLeftAt; i < gpsEntries.length; i++) {
      if (skyDivingEvents.landed.timestamp < gpsEntries[i].timestamp) {
        wasLeftAt = i;
        break;
      }
      flightPlanCoordinates.push(new google.maps.LatLng(gpsEntries[i].latitude, gpsEntries[i].longitude));
  }
  flightPath = new google.maps.Polyline({
  path: flightPlanCoordinates,
  geodesic: true,
  strokeColor: '#00FF00',
  strokeOpacity: 1.0,
  strokeWeight: 2
  });

  flightPath.setMap(map);


  //walking
  flightPlanCoordinates = [];
  for (var i = wasLeftAt; i < gpsEntries.length; i++) {
      flightPlanCoordinates.push(new google.maps.LatLng(gpsEntries[i].latitude, gpsEntries[i].longitude));
  }
  flightPath = new google.maps.Polyline({
  path: flightPlanCoordinates,
  geodesic: true,
  strokeColor: '#000000',
  strokeOpacity: 1.0,
  strokeWeight: 2
  });

  flightPath.setMap(map);
}

var speed = 100;
var serialisedEvents;
var takeOffShown = false;
var takeOffImg = '/static/img/take-off.png';
var freeFallShown = false;
var freeFallImg = '/static/img/freefall.png';

var canopyShown = false;
var canopyImg = '/static/img/canopy.png';
var walkImg = "/static/img/walk.png";

var landedShown = false;
function barometerEvent(eventIndex) {
  var altitude = serialisedEvents[eventIndex].altitude;
  var percentage = (altitude - minAlt)/(maxAlt - minAlt);
  var progress = Math.round(percentage*100);
  $('#current-altitude').text(altitude);
  $('#progress_bar').data('progress', percentage);
  $('#progress_bar').height(progress + "%");
  marker.getIcon().scale = Math.round(((altitude / 100)/5 + 1));
  marker.setIcon(marker.getIcon());
  if (skyDivingEvents.takeoff.timestamp < serialisedEvents[eventIndex].timestamp && !takeOffShown) {
    $('#status-image').attr('src', takeOffImg);
    takeOffShown = true;
  } else if (skyDivingEvents.freefall.timestamp < serialisedEvents[eventIndex].timestamp && !freeFallShown) {
    $('#status-image').attr('src', freeFallImg);
    freeFallShown = true;
  } else if (skyDivingEvents.canopy.timestamp < serialisedEvents[eventIndex].timestamp && !canopyShown) {
    $('#status-image').attr('src', canopyImg);
    canopyShown = true;
  } else if (skyDivingEvents.landed.timestamp < serialisedEvents[eventIndex].timestamp && !landedShown) {
    $('#status-image').attr('src', walkImg);
    landedShown = true;
  }
    
  if (serialisedEvents)
    nextEvent(eventIndex);
}

var previousPosition = null;
function gpsEvent(eventIndex) {
  var lat = serialisedEvents[eventIndex].latitude;
  var lng = serialisedEvents[eventIndex].longitude;
  var position = new google.maps.LatLng(lat, lng);
  if (previousPosition != null) {
    var heading = google.maps.geometry.spherical.computeHeading(previousPosition, position);
    marker.getIcon().rotation = heading;
    marker.setIcon(marker.getIcon());
  }
  previousPosition = position;
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

var skyDivingEvents = null;
function prepareEvents(gpsEntries, altitudeEntries) {

  $('#status-image').attr("src", walkImg);

  serialisedEvents = serialiseEvents(gpsEntries, altitudeEntries);
  var previousTimestamp = serialisedEvents[0].timestamp;
  altitudeEntries = averageBarometerValues(altitudeEntries, 1000);

  skyDivingEvents = identifyFlyingEvents(altitudeEntries);
  
  if (serialisedEvents[0].event_type == "barometer") {
    barometerEvent(0);
  } else if (serialisedEvents[0].event_type == "gps") {
    gpsEvent(0);
  }


}
