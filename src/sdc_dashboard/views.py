from django.shortcuts import render
from .models import SkyDiver, SessionData
from django.utils import simplejson
from django.http import HttpResponse
from SDC import settings
# Create your views here.
def index(request):
    return render(request, 'dashboard.html')


def user_dashboard(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return render(request, 'login.html')
	return render(request, 'dashboard.html')

def get_user_data(request):
	current_user = request.user
	if (not current_user.is_authenticated()):
		return HttpResponse(simplejson.dumps({'message':'authentication error', 'code': 401}), content_type="application/json")

	skydiver = SkyDiver.objects.get(username=current_user.username)
	sessionData = SessionData.objects.get(skyDiver=skydiver)
	data_file = open(settings.DATA_DIR + "/" + sessionData.location)
	data = data_file.readline()
	data_file.close()
	return HttpResponse(data, content_type="application/json")