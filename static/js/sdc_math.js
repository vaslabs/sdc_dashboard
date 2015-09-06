function calculateVerticalVelocity(data, time_density) {
  var velocities = [];
  var initialTime = data[0].timestamp;
  var dx, dt;
  var x1 = data[0].altitude;
  var x2;
  var u;
  var start_timestamp = data[0].timestamp;
  var end_timestamp = start_timestamp + time_density;
  for (var i = 1; i < data.length - 1; i+=1) {
    if (data[i].timestamp > end_timestamp) {
      x2 = data[i].altitude;
      u = (x2-x1)/((data[i].timestamp - start_timestamp)/1000);
      velocities.push([(data[i].timestamp + start_timestamp - (initialTime*2))/2000,u]);
      start_timestamp = data[i].timestamp;
      end_timestamp = data[i].timestamp + time_density;
      x1=x2;
    }
  }

  return velocities;

}

function calculateVerticalVelocityEntries(data, time_density) {

  var velocities = [];
  var initialTime = data[0].timestamp;
  var dx, dt;
  var x1 = data[0].altitude;
  var x2;
  var u;
  var start_timestamp = data[0].timestamp;
  var end_timestamp = start_timestamp + time_density;
  for (var i = 1; i < data.length - 1; i+=1) {
    if (data[i].timestamp > end_timestamp) {
      x2 = data[i].altitude;
      u = (x2-x1)/((data[i].timestamp - start_timestamp)/1000);
      velocities.push({timestamp:(data[i].timestamp + start_timestamp)/2, velocity: u});
      start_timestamp = data[i].timestamp;
      end_timestamp = data[i].timestamp + time_density;
      x1=x2;
    }
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
  if (barometerEntries.length == 0)
    return;
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
    var a, dt, du;
    var cp;
    for (var i = index+1; i < velocityEntries.length; i++) {
      du = velocityEntries[i].velocity - velocityEntries[i-1].velocity;
      dt = velocityEntries[i].timestamp - velocityEntries[i-1].timestamp;
      dt=dt/1000;
      a = du/dt;
      
      if (a > 10) {
        cp = new CanopyEvent(velocityEntries[i].timestamp);
        for (var j = i+1; j < velocityEntries.length; j++) {
          if (velocityEntries[j].velocity > -30 && velocityEntries[j] < 0)
            return new CanopyEvent(velocityEntries[j].timestamp);
        }
      }
    }
    return cp;
  }

  function findLandedEvent(berometerEntries, index) {
    for (var i = index; i < barometerEntries.length; i++) {
      if (Math.abs(barometerEntries[i].altitude - barometerEntries[0].altitude) <= 20) {
        return new LandedEvent(barometerEntries[i].timestamp);
      }
    }
  }


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
var GRAVITY_ACCELERATION = 9.8;
function findMaximumAltitude(barometerValues, beginFrom) {
    var maxBarometerEntry = barometerValues[beginFrom];
    maxBarometerEntry['index'] = beginFrom;
    for (var i = beginFrom + 1; i < barometerValues.length; i++) {
      if (barometerValues[i].altitude > maxBarometerEntry.altitude) {
        maxBarometerEntry = barometerValues[i];
        maxBarometerEntry.index = i;
      }
    }

    //find continuous accelleration
    var index = maxBarometerEntry.index + 1;
    var bv2 = barometerValues[index];
    var bv1 = barometerValues[index-1];

    var speed_1 = (bv2.altitude - bv1.altitude)/((bv2.timestamp - bv1.timestamp)/1000);
    var t_1 = bv2.timestamp;
    var t_2;
    var dt;
    var du;
    var speed_2;
    var persists = 0;
    for (var i = index + 1; i < barometerValues.length; i++) {
      bv2 = barometerValues[i];
      bv1 = barometerValues[i-1];
      speed_2 = (bv2.altitude - bv1.altitude)/((bv2.timestamp - bv1.timestamp)/1000);
      t_2 = bv2.timestamp;
      dt = (t_2 - t_1)/1000;
      du = speed_2 - speed_1;
      var accelleration = du/dt;
      var acc_diff = GRAVITY_ACCELERATION + accelleration;
      if (acc_diff < 3) {
        if (persists >= 3) {
          maxBarometerEntry = barometerValues[i-1];
          maxBarometerEntry.index = i-1;
          return maxBarometerEntry;
        } else {persists++}
      } else {
        persists = 0;
      }
      t_1 = t_2;
    }

    return maxBarometerEntry;
}




function averageBarometerValues(barometerValues, density_milliseconds) {
  
  var avgBarometerEntries = [];
  var altitudeAvg = 0;
  var buffer = [barometerValues[0].altitude];
  var buffer_timestamp = barometerValues[0].timestamp;
  var end_timestamp = barometerValues[0].timestamp + density_milliseconds;
  for (var i=0; i < barometerValues.length; i++) {
    barometerEntry = barometerValues[i];
    if (barometerEntry.timestamp <= end_timestamp) {
      buffer.push(barometerEntry.altitude);
    } else {
      var buffer_sum = sum(buffer);
      avgBarometerEntries.push({'altitude':buffer_sum/buffer.length, 'timestamp':((buffer_timestamp + end_timestamp)/2)});
      buffer = [barometerEntry.altitude];
      buffer_timestamp = barometerEntry.timestamp;
      end_timestamp = buffer_timestamp + density_milliseconds;
    }
  }

  return avgBarometerEntries;

}

function sum(vector) {
  var sum_tmp = 0;
  for (var i = 0; i < vector.length; i++) {
    sum_tmp += vector[i];
  }
  return sum_tmp;
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

function sort_data(skydiving_session) {
    var gpsEntries = skydiving_session.gpsEntries;
    var barometerEntries = skydiving_session.barometerEntries;
    gpsEntries = gpsEntries.sort(function(entryA, entryB) {
         return entryA.timestamp - entryB.timestamp;
    });
    barometerEntries = barometerEntries.sort(function(entryA, entryB) {
         return entryA.timestamp - entryB.timestamp;
    });
    skydiving_session.barometerEntries = barometerEntries;
    skydiving_session.gpsEntries = gpsEntries;
    return skydiving_session;
}

function calculate_metrics(session_data) {
  session_data = sort_data(session_data);
  if (session_data.barometerEntries.length == 0) {
    return {'freefalltime':"N/A", 'exitAltitude':"N/A", 'deploymentAltitude':"N/A", 'maxVelocity':"N/A"};
  }
  
  var avgBarometerEntries = averageBarometerValues(session_data.barometerEntries, 1000);
  
  
  var velocities = calculateVerticalVelocityEntries(avgBarometerEntries, 2000);
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

