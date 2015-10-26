function getLocationDetails(lat, lng, ko_field, callback) {
    var geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(lat, lng);
    geocoder.geocode({'latLng': latlng}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        ko_field(results[0].formatted_address);
      }
    });

    if (callback != null)
    	callback();
}
