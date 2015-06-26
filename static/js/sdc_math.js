function calculateVerticalVelocity(data, sample_skip) {
  var t1, t2, x1, x2;
  var initialTime = data[0].timestamp;
  var velocities = [];
  var dx, dt;
  for (var i = 1; i < data.length - 1; i+=(sample_skip+1)) {
    t1 = data[i-1].timestamp - initialTime;
    t2 = data[i].timestamp - initialTime;
    x1 = data[i-1].altitude;
    x2 = data[i].altitude;
    dt = (t2-t1)/1000;
    dx = (x2-x1);
    var u = dx/dt;
    velocities.push([t2/1000, u]);
  }

  return velocities;

}

function CartesianLocation(x, y, z) {

  var self = this;

  self.x = x;
  self.y = y;
  self.z = z;

  self.distanceFrom = function(other) {
    return Math.sqrt(Math.pow(self.x - other.x, 2) + Math.pow(self.y - other.y, 2) +
           Math.pow(self.z - other.z, 2));
  };

}

function polarToCartesian(lat, lng, alt) {
  var x,y,z;



  return new CartesianLocation(x, y, z);
}

function TakeOffEvent(timestamp) {
  var self = this;
  self.timestamp = timestamp;

}

function FreeFallEvent() {

}

function CanopyEvent() {

}

function LandedEvent() {

}

function identifyFlyingEvents(barometerEntries) {
  var events = {};
  function fastWalkForUp(min_difference, currentIndex, current_altitude) {
    var thisDifference = barometerEntries[currentIndex] - current_altitude;
    if (thisDifference > min_difference) {
      for (var i = currentIndex - 1; i >= 0; i--) {
        thisDifference = barometerEntries[i] - current_altitude;
        if (thisDifference < min_difference) {
          return i+1;
        }
      }
    } else {
      return fastWalkForUp(min_difference, currentIndex + 100, current_altitude);
    }
  }

  function fastWalkForDown(min_difference, currentIndex, current_altitude) {
    var thisDifference = barometerEntries[currentIndex] - current_altitude;
    if (thisDifference < min_difference) {
      for (var i = currentIndex - 1; i >= 0; i--) {
        thisDifference = barometerEntries[i] - current_altitude;
        if (thisDifference > min_difference) {
          return i+1;
        }
      }
    } else {
      return fastWalkForDown(min_difference, currentIndex + 100, current_altitude);
    }
  }

  var slope;

  var current_altitude = barometerEntries[0].altitude;
  var dramaticAltitudeIncreasePoint = fastWalkForUp(300, 0, current_altitude);

  var takeOffTimestamp = barometerEntries[dramaticAltitudeIncreasePoint].timestamp - 30*1000; //go half a minute back

  events['takeoff'] = new TakeOffEvent(takeOffTimestamp);


  var dramaticAltitudeDecrease = fastWalkForDown(-50, dramaticAltitudeIncreasePoint, barometerEntries[dramaticAltitudeIncreasePoint].altitude);

  events['freefall'] = new FreeFallEvent(barometerEntries[dramaticAltitudeDecrease].timestamp);


  return events

}