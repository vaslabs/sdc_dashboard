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

function calculateVerticalVelocityEntries(data, sample_skip) {
  var t1, t2, x1, x2;
  var initialTime = data[0].timestamp;
  var velocities = [];
  var dx, dt;
  velocities.push({timestamp: data[0].timestamp, velocity: 0});
  for (var i = 1; i < data.length - 1; i+=(sample_skip+1)) {
    t1 = data[i-1].timestamp - initialTime;
    t2 = data[i].timestamp - initialTime;
    x1 = data[i-1].altitude;
    x2 = data[i].altitude;
    dt = (t2-t1)/1000;
    dx = (x2-x1);
    var u = dx/dt;
    velocities.push({timestamp: data[i].timestamp, velocity: u});
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

function FreeFallEvent(timestamp, altitude) {
  var self = this;
  self.timestamp = timestamp;
  self.altitude = altitude;
}

function CanopyEvent(timestamp) {
  var self = this;
  self.timestamp = timestamp;

}

function LandedEvent(timestamp) {
  var self = this;
  self.timestamp = timestamp;
}

function identifyFlyingEvents(barometerEntries) {
  var events = {};
  function fastWalkForUp(min_difference, currentIndex, current_altitude) {
    if (currentIndex >= barometerEntries.length) {
      currentIndex /= 2;
    }
    var thisDifference = barometerEntries[currentIndex].altitude - current_altitude;
    if (thisDifference > min_difference) {
      for (var i = currentIndex - 1; i >= 0; i--) {
        thisDifference = barometerEntries[i].altitude - current_altitude;
        if (thisDifference < min_difference) {
          return i+1;
        }
      }
      return currentIndex;
    } else {
      return fastWalkForUp(min_difference, currentIndex + 100, current_altitude);
    }
  }

  function fastWalkForDown(min_difference, currentIndex, current_altitude) {
    if (currentIndex >= barometerEntries.length) {
      currentIndex = currentIndex / 2;
      console.log(currentIndex);
    }
    var thisDifference = barometerEntries[currentIndex].altitude - current_altitude;

    if (thisDifference < min_difference) {
      for (var i = currentIndex - 1; i >= 0; i--) {
        thisDifference = barometerEntries[i].altitude - current_altitude;
        if (thisDifference > min_difference) {
          return i+1;
        }
      }
      return currentIndex;
    } else {
      return fastWalkForDown(min_difference, currentIndex + 100, current_altitude);
    }
  }

  function findCanopyEvent(maxSpeed, velocityEntries, index) {
    
    if (velocityEntries[index].velocity > maxSpeed.velocity*0.2)
      return new CanopyEvent(velocityEntries[index].timestamp);
    return findCanopyEvent(maxSpeed, velocityEntries, index+1);
  }

  function findLandedEvent(berometerEntries, index) {
    for (var i = index; i < barometerEntries.length; i++) {
      if (Math.abs(barometerEntries[i].altitude - barometerEntries[0].altitude) <= 20) {
        return new LandedEvent(barometerEntries[i].timestamp);
      }
    }
  }

  var slope;

  var current_altitude = barometerEntries[0].altitude;
  var dramaticAltitudeIncreasePoint = fastWalkForUp(20, 0, current_altitude);

  var takeOffTimestamp = barometerEntries[dramaticAltitudeIncreasePoint].timestamp; //go half a minute back

  events['takeoff'] = new TakeOffEvent(takeOffTimestamp);
  var maximumAltitude = findMaximumAltitude(barometerEntries, dramaticAltitudeIncreasePoint);

  var dramaticAltitudeDecrease = fastWalkForDown(-30, maximumAltitude.index, maximumAltitude.altitude);

  events['freefall'] = new FreeFallEvent(barometerEntries[dramaticAltitudeDecrease].timestamp, 
                                         barometerEntries[dramaticAltitudeDecrease].altitude);

  var velocityEntries = calculateVerticalVelocityEntries(barometerEntries, 50);


  var maximumSpeed = findMaximumSpeed(velocityEntries);


  events.canopy = findCanopyEvent(maximumSpeed, velocityEntries, maximumSpeed.index); 
  
  events.landed = findLandedEvent(barometerEntries, maximumAltitude.index);
  return events

}

function findMaximumAltitude(barometerValues, beginFrom) {
  var maxBarometerEntry = barometerValues[beginFrom];
  maxBarometerEntry['index'] = beginFrom;
  for (var i = beginFrom + 1; i < barometerValues.length; i++) {
    if (barometerValues[i].altitude > maxBarometerEntry.altitude) {
      maxBarometerEntry = barometerValues[i];
      maxBarometerEntry.index = i;
    }
  }

    return maxBarometerEntry;
}




function averageBarometerValues(barometerValues, density) {
  var avgBarometerEntries = []; 
  var timestampAvg = 0;
  var altitudeAvg = 0;
  for (var i = 0; i < barometerValues.length - density; i+=density) {
    for (var j = 0; j < density; j++) {
      timestampAvg += barometerValues[i+j].timestamp/density;
      altitudeAvg += barometerValues[i+j].altitude/density;
    }
    avgBarometerEntries.push({timestamp:timestampAvg, altitude: altitudeAvg});
    timestampAvg = 0;
    altitudeAvg = 0;
  }

  return avgBarometerEntries;

}


function findMaximumSpeed(velocityEntries) {
  var maxSpeed = null;
  for (var i = 1; i < velocityEntries.length; i++) {
    if (velocityEntries[i].velocity < 0) {
      if ( maxSpeed == null ) {
        maxSpeed = velocityEntries[i];
        maxSpeed.index = i;
      } else if (velocityEntries[i].velocity < maxSpeed.velocity) {
        maxSpeed = velocityEntries[i];
        maxSpeed.index = i;
      }
    }
  }
  return maxSpeed;
}

function calculate_metrics(session_data) {
  var avgBarometerEntries = averageBarometerValues(session_data.barometerEntries, 3);
  if (avgBarometerEntries.length == 0 ) {
      return {'freefalltime':"N/A", 'exitAltitude':"N/A", 'deploymentAltitude':"N/A", 'maxVelocity':"N/A"};

  }
  var velocities = calculateVerticalVelocityEntries(avgBarometerEntries, 50);
  var max_speed = findMaximumSpeed(velocities); //logbooked
  var events = identifyFlyingEvents(avgBarometerEntries);  
  var totalFreeFallTime = (events.canopy.timestamp - events.freefall.timestamp)/1000; //logbooked
  var exitAltitude = events.freefall.altitude;
  var deploymentAltitude;
  for (var i = 0; i < avgBarometerEntries.length; i++) {
    if (avgBarometerEntries[i].timestamp > events.canopy.timestamp) {
      deploymentAltitude = avgBarometerEntries[i].altitude;
      break;
    }
  }

  return {'freefalltime':totalFreeFallTime.toFixed(2), 'exitAltitude':exitAltitude.toFixed(2), 
          'deploymentAltitude':deploymentAltitude.toFixed(2), 'maxVelocity':max_speed.velocity.toFixed(2)};

}

