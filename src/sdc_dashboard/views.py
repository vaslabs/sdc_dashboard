from django.shortcuts import render, redirect
from .models import SkyDiver, SessionData, ShareLink
import json, string, random
from django.http import HttpResponse
from SDC import settings
import datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from sdc_utils import fetch_logbook

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
	token_key = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
	token = Token.objects.get(key=token_key)
	current_user = token.user
	received_json_data=json.loads(request.body)
	date_submitted = datetime.datetime.now()
	file_name = current_user.username + str(date_submitted.time()) + '.json'
	data_file = open(settings.DATA_DIR + "/" + file_name, 'w')
	data_file.write(json.dumps(received_json_data))
	data_file.close()
	skydiver = SkyDiver.objects.get(username=current_user.username)
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

