from .models import SkyDiver, SessionData
from rest_framework.authtoken.models import Token

def get_skydiver_from_token(request):
	token_key = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
	return from_token(token_key)

def from_token(token_key):
	token = Token.objects.get(key=token_key)
	print token
	current_user = token.user
	skydiver = SkyDiver.objects.get(username=current_user.username)

	return {'user':current_user, 'skydiver':skydiver}

def getSessionList(skydiver):
	sessionDataList = SessionData.objects.filter(skyDiver=skydiver)
	return sessionDataList
