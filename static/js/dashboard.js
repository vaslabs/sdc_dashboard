function getMyData() {
  var url = '/dashboard/session';
  var currentURLParts = document.URL.split('/');
  var sessionId;
  var logBookPresent = -1;
  for (var i = 0; i < currentURLParts.length; i++) {
    if (currentURLParts[i] == "logbook")
      logBookPresent = i;
  }
  if (logBookPresent >= 0 && logBookPresent < currentURLParts.length - 1) {
    sessionId = currentURLParts[logBookPresent+1];
    url += "/" + sessionId;
    $("a#charts").attr({'href':'/dashboard/graphs/'+sessionId});
  }

  getJSONResponse(url, initialize);
}

var map;
var myData;
function initialize(data) {
  data = sort_data(data);
  var latitude = data.gpsEntries[0].latitude;
  var longitude = data.gpsEntries[0].longitude;
  var mapOptions = {
    center: { lat: latitude, lng: longitude},
    zoom: 16
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
  myData = data;
  setUpControlPanel();
}
google.maps.event.addDomListener(window, 'load', getMyData);


function showLink(link_data) {
  var linkId = link_data.link;
  $('p#link-share').text("http://" + location.host + "/dashboard/shared_session/l/" + linkId);
  $('#dialog').css("display", "block");
  $('#dialog').dialog();
}

function setUpControlPanel() {
  $('#session-path-button').click(function() {
    drawPath(myData);
  });

  $('#animation-button').click(function() {
    startAnimating(myData);
  });
  $('#real-speed-button').click(function() {
    speed = 1;
  });
  $('#fast-forward-button').click(function() {
    speed = 100;
  });

  $('#share-session-button').click(function() {
    getJSONResponse('/dashboard/share', showLink);
  });
}

$(document).ready(function() {
   $('#simple-menu').sidr({
      side: 'right'
   });
});
