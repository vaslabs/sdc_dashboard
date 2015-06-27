from django.shortcuts import render, redirect
from .models import SkyDiver, SessionData, ShareLink
import json, string, random
from django.http import HttpResponse
from SDC import settings
import datetime
# Create your views here.
def index(request):
	return user_dashboard(request)


def user_dashboard(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return redirect('/login')
	return render(request, 'dashboard.html')

def get_user_data(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return HttpResponse(json.dumps({'message':'authentication error', 'code': 401}), content_type="application/json")

	skydiver = SkyDiver.objects.get(username=current_user.username)
	sessionData = SessionData.objects.filter(skyDiver=skydiver)
	data_file = open(settings.DATA_DIR + "/" + sessionData[len(sessionData) - 1].location)
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

