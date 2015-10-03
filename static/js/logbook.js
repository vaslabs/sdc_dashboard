function validateValue(value) {
  return value == 'N/A' ? 0 : value;
}

function validateReverseValue(value) {
  return value == 0 || value == 'N/A' ? 'N/A' : value;
}

function SkydivingSession(date, number, metrics, location, location_name, notes, id, fromRaw) {
  var self = this;
  self.date = ko.observable(date);
  self.number = ko.observable(number);
  self.freefalltime = ko.observable(validateReverseValue(metrics.freefalltime));
  self.exitAltitude = ko.observable(validateReverseValue(metrics.exitAltitude));
  self.deploymentAltitude = ko.observable(validateReverseValue(metrics.deploymentAltitude));
  self.maxVelocity = ko.observable(validateReverseValue(metrics.maxVelocity));
  self.latitude = location.lat;
  self.longitude = location.lng;
  self.location_name = ko.observable(location_name);
  if (self.location_name() == null) {
    getLocationDetails(self.latitude, self.longitude, self.location_name, null);
  }
  self.notes = ko.observable(notes);
  self.id = id;
  self.fromRaw = fromRaw;
  self.save = function() {
    var logbook_data = {
                   'id':self.id,
                   'date':self.date().getTime(),
                   'freefalltime':validateValue(self.freefalltime()),
                   'exitAltitude':validateValue(self.exitAltitude()),
                   'deploymentAltitude':validateValue(self.deploymentAltitude()),
                   'maxVerticalVelocity':validateValue(self.maxVelocity()),
                   'latitude':self.latitude,
                   'longitude':self.longitude,
                   'location_name':self.location_name(),
                   'notes':self.notes(),
                   'fromRaw':self.fromRaw
               };
      $.ajax({
      url: '/logbook/save/',
      type: 'post',
      dataType: 'json',
      success: function (data) {
        console.log(data);
      },
      data: logbook_data
  });


  }
}

function initialize(session_data) {

  var sessions = ko.observableArray();
  for (var i = session_data.length - 1; i >= 0; i--) {
    if ('raw' in session_data[i]) {
      var session = session_data[i]['raw'];
      var date = new Date(session.gpsEntries[0].timestamp)
      var metrics = calculate_metrics(session);
      var location = {lat:session.gpsEntries[0].latitude, lng: session.gpsEntries[0].longitude};
      var ss = new SkydivingSession(date, i, metrics, location, null, "", session_data[i]['id'], true);
      ss.timestamp = session.gpsEntries[0].timestamp;
      sessions.push(ss);
    } else {
      var date = new Date(session_data[i].timeInMillis)
      var metrics = session_data[i].metrics;
      var location = {lat: session_data[i].latitude, lng: session_data[i].longitude};
      var ss = new SkydivingSession(date, i, metrics, location, session_data[i].location, session_data[i].notes, session_data[i].id, false)
      ss.timestamp = session_data[i].timeInMillis;
      sessions.push(ss);
    }

    sessions = sessions.sort(function(a,b) {
      return a.id - b.id;
    });

  }

  prepareUI(sessions);
}


var model;
function prepareUI(sessions) {
   model = {"sessions":sessions};
   ko.applyBindings(model);
}

function getMyData() {  
  getJSONResponse('/dashboard/logbook_entries', initialize);
}

$(function() {
  getMyData();
});