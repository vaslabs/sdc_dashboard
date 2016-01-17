# Create your views here.

from django.shortcuts import render
import json, string, random
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .temp_account_utils import create_temporary_account, encrypt, getAccount, saveData, getSessions, getSession
from rest_framework.decorators import api_view
from django.core.serializers.json import DjangoJSONEncoder
from sdc_dashboard.api_utils import from_token, getSessionList
from sdc_dashboard import api_utils
from sdc_dashboard.views import save_session_data, get_user_data
from sdc_dashboard.sdc_utils import logbookRawData


def ok_message():
	return HttpResponse("{'message':'OK', 'code': 200}", content_type="application/json")

def authentication_error():
	return HttpResponse("{'message':'ERROR', 'code': 401}", content_type="application/json")

@csrf_exempt
@api_view(['POST'])
def create_account(request):
	received_json_data=json.loads(request.body)
	publicKey = received_json_data["publicKey"]
	print publicKey
	account, token = create_temporary_account(publicKey)
	encrypted_token = encrypt(account, token.token)
	response = {}
	response['apitoken'] = encrypted_token
	body = json.dumps(response)
	return HttpResponse(body, content_type="application/json")


@csrf_exempt
def save_session(request):
	try:
		user, isReal = getUser(request)
		if isReal:
			return save_session_data(request)
		temporaryUser = user
	except:
		return authentication_error()
	if (temporaryUser != None):
		saveData(temporaryUser, request.body)
		return ok_message()
	else:
		return authentication_error()

def getUser(request):
	apitoken = 	request.META['HTTP_AUTHORIZATION'].split(' ')[1]
	try:
		realUserData = from_token(apitoken)
		if (realUserData['skydiver'] != None):
			return realUserData['skydiver'], True
	except Exception as e:
		print e
	temporaryUser = getAccount(apitoken)
	return temporaryUser, False

def sessionListToJsonResponse(sessions):
	data = []
	for session in sessions:
		jsession = {}
		jsession['id'] = session.id
		jsession['submittedDate'] = session.submittedDate
		data.append(jsession)
	jsonResponse = json.dumps(data, cls=DjangoJSONEncoder)
	return HttpResponse(jsonResponse, content_type="application/json")


def get_session_list(request):
	try:
		user, isReal = getUser(request)
		if isReal:
			sessions = getSessionList(user)
			return sessions
	except Exception as e:
		print e
		return authentication_error()

	sessions = getSessions(user)
	return sessions


@csrf_exempt
def get_sessions(request):
	sessions = get_session_list(request)

	return sessionListToJsonResponse(sessions)

@csrf_exempt
def get_session(request, sessionId):
	try:
		user, isReal = getUser(request)
		if isReal:
			return get_user_data(request, sessionId)
	except:
		return authentication_error()
	session = getSession(user, sessionId)

	return HttpResponse(session, content_type="application/json")

@csrf_exempt
def get_all_data(request):
	session_entries = get_session_list(request)
	data = []

	for session_entry in session_entries:
		data.append(logbookRawData(session_entry))

	jsonResponse = json.dumps(data)
	return HttpResponse(jsonResponse, content_type="application/json")

