from django.shortcuts import render, redirect
from .models import SkyDiver, SessionData, ShareLink
import json, string, random
from django.http import HttpResponse
from SDC import settings
import datetime
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
	sessionNo = int(sessionNo)
	if (sessionNo < 0) or (sessionNo >= len(sessionData)):
		print "sessionNo:", sessionNo
		sessionNo = len(sessionData) - 1
	data_file = open(settings.DATA_DIR + "/" + sessionData[sessionNo].location)
	data = data_file.readline()
	data_file.close()
	print sessionNo
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
