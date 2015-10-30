from .models import Logbook, SessionData
from SDC import settings
import json

def fetch_logbook(skydiver):
	logbookObjects = Logbook.objects.filter(skyDiver=skydiver)
	logbookEntries = [json.loads(l.__str__()) for l in logbookObjects]

	sessionEntries = fetch_mysessions(skydiver)
	exclude_list = [logbookObject.sessionData for logbookObject in logbookObjects]
	selectedSessionEntries = [ sessionEntry for sessionEntry in sessionEntries if sessionEntry not in exclude_list]

	for sessionEntry in selectedSessionEntries:
		logbookEntries.append({'raw':logbookRawData(sessionEntry), "id":sessionEntry.id, "timestamp":str(sessionEntry.timestamp)})
	return logbookEntries


#lets avoid heavy computations on the server for now,
#client can compute it for us and send the results back
def logbookRawData(sessionEntry):
	data_file = open(settings.DATA_DIR + "/" + sessionEntry.location)
	data = data_file.readline()
	data_file.close()
	return json.loads(data)


def fetch_logbook_no_raw(skydiver):
	logbookObjects = Logbook.objects.filter(skyDiver=skydiver)
	logbookEntries = [json.loads(l.__str__()) for l in logbookObjects]
	return logbookEntries

def fetch_mysessions(skydiver):
	return sorted([ normaliseSessionEntry(sessionData) for sessionData in SessionData.objects.filter(skyDiver=skydiver)], key=lambda x: x.timestamp)

def normaliseSessionEntry(sessionEntry):
	if (sessionEntry.timestamp == 0):
		raw_data = logbookRawData(sessionEntry)
		print raw_data['gpsEntries']
		if ('gpsEntries' in raw_data and len(raw_data['gpsEntries']) > 0):
			sessionEntry.timestamp = raw_data['gpsEntries'][0]['timestamp']
		else:
			sessionEntry.timestamp = raw_data['barometerEntries'][0]['timestamp']
		sessionEntry.save()
	return sessionEntry