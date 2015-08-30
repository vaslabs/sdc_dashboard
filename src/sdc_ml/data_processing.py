import json
from math import cos, sin, radians, fabs, asin, sqrt, atan2
from itertools import izip, islice
from operator import attrgetter

class Entry(object):

    def __init__(self, time):
        self.time = time

        
class BarometerEntry(Entry):

    def __init__(self, kwargs):
        self.alt = kwargs['altitude']
        super(BarometerEntry, self).__init__(kwargs['timestamp'])


class GpsEntry(Entry):

    def __init__(self, kwargs):
        self.lat = kwargs['latitude']
        self.lon = kwargs['longitude']
        super(GpsEntry, self).__init__(kwargs['timestamp'])


class Coordinate(object):

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return str(self.lat) + " " + str(self.lon)

    def __eq__(self, other):
        return self.lat == other.lat and self.lon == other.lon


class Event(object):

    def __init__(self, time, lat, lon, alt):
        self.time = time
        self.alt = alt
        self.coord = Coordinate(lat, lon)
        self.hspeed = 0.0
        self.vspeed = 0.0

    def __str__(self):
        return ", ".join([str(self.time), str(self. alt), str(self.coord.lat),
                           str(self.coord.lon)])


    
def select_attrs(events, attrs):
    # events :: [Event]
    # attrs :: [String]
    #
    # returns :: [(attr_1, attr_2, ..., attr_n)]

    def get_attrs(event, getters):
        return tuple(g(event) for g in getters)
    
    getters = [attrgetter(a) for a in attrs]

    return list(get_attrs(event, getters) for event in events)


def rwindow(xs, n):
    # generator for rolling window, will generate as many items as xs
    
    result = tuple(islice(xs, n))
    
    if len(result) == n:
        yield result    
    for elem in xs:
        result = result[1:] + (elem,)
        yield result

        
def window(xs, n):
    # generator for moving window, will generate xs/n items
    for i in range(0, len(xs), n):
        result = tuple(islice(xs[i:], n))
        yield result

        
def average_speeds(events, n):
    # events :: [Event]
    # n :: Int
    #
    # returns [(Float, Float)]
    def aspeeds(w):
        hss = list(e.hspeed for e in w)
        vss = list(e.vspeed for e in w)

        return sum(hss)/len(hss), sum(vss)/len(vss)
    
    return list(aspeeds(w) for w in window(events, n))

        
def calc_hdist(coord1, coord2):
    if coord1 == coord2: return 0.0
    lat1, lon1 = coord1.lat, coord1.lon
    lat2, lon2 = coord2.lat, coord2.lon
    radius = 6371000

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c

    return d


def calc_hspeed(entry1, entry2):
    hdist = calc_hdist(entry1.coord, entry2.coord)
    dt = entry2.time - entry1.time

    return (hdist / dt)


def calc_vspeed(entry1, entry2):
    vdist = entry2.alt - entry1.alt
    dt = entry2.time - entry1.time
    
    return (vdist / dt)

        
def calc_speeds(events):
    #events:: [Event]
    #
    # returns [Event]
    hspeeds = list(calc_hspeed(e, e1) for e, e1 in izip(events, events[1:]))
    vspeeds = list(calc_vspeed(e, e1) for e, e1 in izip(events, events[1:]))

    for e, hs, vs in izip(events, hspeeds, vspeeds):
        e.hspeed = hs
        e.vspeed = vs

    return events


def combine_tseries(entries):
    # entries:: [Entry]
    # returns [Event]

    events = list()

    def find_first_instance(entries, T):
        for e in entries:
            if isinstance(e, T): return e

    current_gps = find_first_instance(entries, GpsEntry)
    current_bar = find_first_instance(entries, BarometerEntry)

    for e in entries:
        if isinstance(e, BarometerEntry):
            current_bar = e
        elif isinstance(e, GpsEntry):
            current_gps = e
            events.append(Event(e.time, current_gps.lat, current_gps.lon,
                                   current_bar.alt))

    return events


def merge_entries(bar_entries, gps_entries):
    # bar_entries:: [BarometerEntry]
    # gps_entries:: [GpsEntry]
    # returns [Entry]
    
    all_entries = bar_entries + gps_entries

    return sorted(all_entries, key=lambda x: x.time)
    

def get_entries(js):
    # js :: python repr of a json object
    # returns ([BarometerEntry], [GpsEntry])

    bentries = list(BarometerEntry(be) for be in js['barometerEntries'])
    gentries = list(GpsEntry(ge) for ge in js['gpsEntries'])

    return bentries, gentries


def get_events(js):
    bar_entries, gps_entries = get_entries(js)
    all_entries = merge_entries(bar_entries, gps_entries)

    events = combine_tseries(all_entries)
    events = calc_speeds(events)

    return events
