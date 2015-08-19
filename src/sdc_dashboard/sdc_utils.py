from .models import Logbook, sessionData


def fetch_logbook(skydiver):
	logbookEntries = Logbook.objects.filter(skyDiver=skydiver)
	sessionEntries = SessionData.objects.filter(skyDiver=skydiver).exclude(sessionData in [ l.sessionData for l in logbookEntries ])
	for sessionEntry in sessionEntries:
		logbookEntry.append({'raw':logbookRawData(sessionEntry)})

	return logbookEntries


#lets avoid heavy computations on the server for now,
#client can compute it for us and send the results back
def logbookRawData(sessionEntry):
	data_file = open(settings.DATA_DIR + "/" + sessionEntry.location)
	data = data_file.readline()
	data_file.close()
	return data
