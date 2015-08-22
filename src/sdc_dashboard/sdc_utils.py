from .models import Logbook, SessionData
from SDC import settings
import json

def fetch_logbook(skydiver):
	logbookEntries = list(Logbook.objects.filter(skyDiver=skydiver))
	print logbookEntries
	sessionEntries = SessionData.objects.filter(skyDiver=skydiver)
	exclude_list = [logbookEntry.sessionData for logbookEntry in logbookEntries]
	selectedSessionEntries = [ sessionEntry for sessionEntry in sessionEntries if sessionEntry not in exclude_list]

	for sessionEntry in selectedSessionEntries:
		logbookEntries.append({'raw':logbookRawData(sessionEntry)})

	return logbookEntries


#lets avoid heavy computations on the server for now,
#client can compute it for us and send the results back
def logbookRawData(sessionEntry):
	data_file = open(settings.DATA_DIR + "/" + sessionEntry.location)
	data = data_file.readline()
	data_file.close()
	return json.loads(data)
