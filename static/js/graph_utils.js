function serialiseEvents(gpsEntries, barometerEntries, gpsCallback, barometerCallback) {
    
    var event_array = [];
    var barometerIndex = 0;
    for (var i = 0; i < gpsEntries.length; i++) {
        gpsNextTimestamp = gpsEntries[i];
        barometerNextTimestamp = barometerEntries[barometerIndex];
        while (gpsNextTimestamp >= barometerNextTimestamp) {
            var eventFunction = function() {
                barometerCallback(barometerEntries[barometerIndex].altitude);
            };
            event_array.push({timestamp: barometerNextTimestamp, eventCall: eventFunction});
            barometerIndex += 1;
            barometerNextTimestamp = barometerEntries[barometerIndex].timestamp;
        }//while
        var eventFunction = function() {
            gpsCallback(gpsEntries[i].latitude, gpsEntries[i].longitude);
        };

        event_array.push({timestamp: gpsNextTimestamp, eventCall: eventFunction});
    }//for

    for (var i = barometerIndex; i < barometerEntries.length; i++) {
        var eventFunction = function() {
            barometerCallback(barometerEntries[i].altitude);
        };
        event_array.push({timestamp: barometerNextTimestamp, eventCall: eventFunction});
    }

    return event_array;
}