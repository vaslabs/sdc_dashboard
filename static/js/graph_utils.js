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