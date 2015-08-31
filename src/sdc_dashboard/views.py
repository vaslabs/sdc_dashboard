from django.shortcuts import render, redirect
from .models import SkyDiver, SessionData, ShareLink, Location, Logbook
import json, string, random
from django.http import HttpResponse
from SDC import settings
import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import api_utils
from django.views.decorators.csrf import csrf_exempt
from sdc_utils import fetch_logbook, fetch_logbook_no_raw
from datetime import datetime
from rest_framework.authtoken.models import Token

# Create your views here.
def index(request):
	return user_dashboard(request)


def user_dashboard(request, sessionNo=0):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return redirect('/login')
	return render(request, 'dashboard.html')


def get_user_data(request, sessionNo=-1):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return HttpResponse(json.dumps({'message':'authentication error', 'code': 401}), content_type="application/json")

	skydiver = SkyDiver.objects.get(username=current_user.username)
	
	sessionData = SessionData.objects.filter(skyDiver=skydiver)
	try:
		sessionNo = int(sessionNo)
	except:
		sessionNo = len(sessionData) - 1
	if (sessionNo < 0) or (sessionNo >= len(sessionData)):
		sessionNo = len(sessionData) - 1
	data_file = open(settings.DATA_DIR + "/" + sessionData[sessionNo].location)
	data = data_file.readline()
	data_file.close()
	return HttpResponse(data, content_type="application/json")

def load_user_graphs(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return redirect('/login')
	return render(request, 'graphs.html')

def share_latest_dive(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return HttpResponse(json.dumps({'message':'authentication error', 'code': 401}), content_type="application/json")
	skydiver = SkyDiver.objects.get(username=current_user.username)
	linkId = id_generator()
	expiryDate = datetime.datetime.now() + datetime.timedelta(days=5)
	sharelink = ShareLink(shareLink=linkId, userShared=skydiver, expires=expiryDate)
	try:
		sharelink.save()
		return_value={"link":sharelink.shareLink}
	except Exception as e:
		return_value={"error":str(e)}
	return HttpResponse(json.dumps(return_value), content_type="application/json")


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def view_shared_session(request, linkid):
	return render(request, 'shared_dashboard.html')

def get_shared_session(request, linkid):
	return_value = {}
	try:
		sharedLink = ShareLink.objects.get(shareLink=linkid)
		sessionData = SessionData.objects.filter(skyDiver=sharedLink.userShared)
		data_file = open(settings.DATA_DIR + "/" + sessionData[len(sessionData) - 1].location)
		data = data_file.readline()
		data_file.close()
		return HttpResponse(data, content_type="application/json")
	except:
		return_value = {"error":"500"}
		return HttpResponse(json.dumps(return_value), content_type="application/json")


def get_user_sessions(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return HttpResponse(json.dumps({'message':'authentication error', 'code': 401}), content_type="application/json")

	skydiver = SkyDiver.objects.get(username=current_user.username)
	sessionData = SessionData.objects.filter(skyDiver=skydiver)
	sessions = [];
	for session in sessionData:
		data_file = open(settings.DATA_DIR + "/" + session.location)
		json_session = json.load(data_file)
		data_file.close()
		sessions.append(json_session)

	return HttpResponse(json.dumps(sessions), content_type="application/json")

def get_logbook_screen(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return redirect('/login')
	return render(request, 'logbook.html')


def get_api_token(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return HttpResponse(json.dumps({'message':'authentication error', 'code': 401}), content_type="application/json")
	token = Token.objects.get(user=current_user)
	response_json = {"token":token.key}
	return HttpResponse(json.dumps(response_json), content_type="application/json")


@csrf_exempt
def save_session_data(request, format=None):
	user_details = api_utils.get_skydiver_from_token(request)
	current_user = user_details['user']
	received_json_data=json.loads(request.body)
	date_submitted = datetime.now()
	file_name = current_user.username + str(date_submitted.time()) + '.json'
	data_file = open(settings.DATA_DIR + "/" + file_name, 'w')
	data_file.write(json.dumps(received_json_data))
	data_file.close()
	skydiver = user_details['skydiver']
	sessionData = SessionData(skyDiver=skydiver, submittedDate=date_submitted, location = file_name)
	sessionData.save()
	return HttpResponse(json.dumps({'message':'OK', 'code': 200}), content_type="application/json")
 
def get_qrcode_api(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return redirect('/login')
	return render(request, 'api.html')

def get_demo_page(request):
	return render(request, 'demo.html')

def get_demo_data(request):
	return_value = {}
	try:
		data_file = open(settings.DATA_DIR + "/stephanie_2015_06_21.json")
		data = data_file.readline()
		data_file.close()
		return HttpResponse(data, content_type="application/json")
	except:
		return_value = {"error":"500"}
		return HttpResponse(json.dumps(return_value), content_type="application/json")	



def get_logbook_entries(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return redirect('/login')

	skydiver = SkyDiver.objects.get(username=current_user.username)

	return_value = fetch_logbook(skydiver)
	return HttpResponse(json.dumps(return_value), content_type="application/json")

@csrf_exempt
def save_logbook(request):
	current_user = request.user
	if request.method == 'GET':
		return HttpResponse(json.dumps({'error':"Not supported method"}))
	if (not current_user.is_authenticated()):
		return HttpResponse(json.dumps({'message':'authentication error', 'code': 401}), content_type="application/json")

	skydiver = SkyDiver.objects.get(username=current_user.username)
	logbook_json = request.POST
	if (logbook_json["fromRaw"] == 'true'):
		return save_first_time_logbook(logbook_json, skydiver)
	else:
		return overwrite_logbook(logbook_json, skydiver)


def save_first_time_logbook(logbook_data, skydiver):
	print logbook_data
	sessionID = logbook_data['id']
	sessionData = validateSessionId(sessionID, skydiver)
	if (sessionData == None):
		return HttpResponse(json.dumps({'message':'authentication error. Don\'t be sneaky', 'code': 401}), content_type="application/json")
	try:
		location = Location.objects.get(latitude=sessionData['latitude'], longitude=sessionData['longitude'], name=sessionData['location_name'])
	except:
		location = Location(latitude=logbook_data['latitude'], longitude=logbook_data['longitude'], name=logbook_data['location_name'])
		location.save()
	dateOfSession = datetime.fromtimestamp(int(logbook_data['date'])/1000)
	logbook = Logbook(skyDiver=skydiver, sessionData=sessionData, location=location, freeFallTime=logbook_data['freefalltime'], \
		exitAltitude=logbook_data['exitAltitude'], deploymentAltitude=logbook_data['deploymentAltitude'], maxVerticalVelocity=logbook_data['maxVerticalVelocity'],\
		date=dateOfSession, notes=logbook_data['notes'])
	try:
		logbook.save()
		return HttpResponse(json.dumps({"message":"OK"}), content_type="application/json")
	except Exception as e:
		print e
		return HttpResponse(json.dumps({"message":"OOoops!", "code":500}), content_type="application/json")

def overwrite_logbook(logbook_json, skydiver):
	
	try:
		logbook = Logbook.objects.get(skyDiver=skydiver, id=logbook_json['id'])
	except Exception as e:
		print e
		return HttpResponse(json.dumps({'message':'authentication error. Don\'t be sneaky', 'code': 401}), content_type="application/json")

	return update_logbook(logbook, logbook_json)

def validateSessionId(sessionId, skydiver):
	try:
		sessionData = SessionData.objects.get(skyDiver=skydiver, id=sessionId)
	except:
		return None
	return sessionData 



def update_logbook(logbook, data):
	logbook.notes = data["notes"]
	logbook.save()
	return HttpResponse(json.dumps({"message":"OK"}), content_type="application/json")


@csrf_exempt
def get_logbook_entries_api(request):
	user_details = api_utils.get_skydiver_from_token(request)
	skydiver = user_details['skydiver']
	try:
		return_value = fetch_logbook_no_raw(skydiver)
	except Exception as e:
		print e
		return_value = {'error':'Nothing found'}

	return HttpResponse(json.dumps(return_value), content_type="application/json")

