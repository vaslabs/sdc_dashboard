function calculateVerticalVelocity(data, sample_skip) {
  var t1, t2, x1, x2;
  var initialTime = data[0].timestamp;
  var velocities = [];
  var dx, dt;
  for (var i = 1; i < data.length - 1; i+=sample_skip) {
    t1 = data[i-1].timestamp - initialTime;
    t2 = data[i].timestamp - initialTime;
    x1 = data[i-1].altitude;
    x2 = data[i].altitude;
    dt = (t2-t1)/1000;
    dx = (x1-x2);
    var u = dx/dt;
    if (u < 0)
      console.log(t2, t1, x1, x2);
    velocities.push([t2/1000, u]);
  }

  return velocities;

}

function CartesianLocation(x, y, z) {

  var self = this;

  self.x = x;
  self.y = y;
  self.z = z;

  self.distanceFrom = function(CartesianLocation other) {
    return Math.sqrt(Math.pow(self.x - other.x, 2) + Math.pow(self.y - other.y, 2) +
           Math.pow(self.z - other.z, 2));
  };

}

function polarToCartesian(lat, lng, alt) {
  var x,y,z;



  return new CartesianLocation(x, y, z);
}

