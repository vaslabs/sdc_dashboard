function serialiseEvents(gpsEntries, barometerEntries, gpsCallback, barometerCallback) {
    
    var event_array = [];
    var barometerIndex = 0;
    var gpsIndex = 0;
    while (barometerIndex < barometerEntries.length && gpsIndex < gpsEntries.length) {
        if (gpsEntries[gpsIndex].timestamp <= barometerEntries[barometerIndex].timestamp) {
            event_array.push({timestamp: gpsEntries[gpsIndex].timestamp, event_type: "gps",  latitude: gpsEntries[gpsIndex].latitude, 
                                                                               longitude: gpsEntries[gpsIndex].longitude});
            gpsIndex++;
        } else {
            event_array.push({timestamp: barometerEntries[barometerIndex].timestamp, event_type: "barometer", 
                              altitude: barometerEntries[barometerIndex].altitude});
            barometerIndex++;

        }
    }
    for (var i = barometerIndex; i < barometerEntries.length; i++) {

        event_array.push({timestamp: barometerEntries[i].timestamp, event_type: "barometer", altitude: barometerEntries[i].altitude});
    }

    for (var i = gpsIndex; i < gpsEntries.length; i++) {
        event_array.push({timestamp: gpsEntries[i].timestamp, event_type: "gps",  latitude: gpsEntries[i].latitude, 
                                                                               longitude: gpsEntries[i].longitude});    
    }
    return event_array;
}

