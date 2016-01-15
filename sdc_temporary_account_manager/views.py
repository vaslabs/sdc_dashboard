# Create your views here.

from django.shortcuts import render
import json, string, random
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .temp_account_utils import create_temporary_account, encrypt, getAccount
from rest_framework.decorators import api_view

def ok_message():
	return HttpResponse("{'message':'OK', 'code': 200}", content_type="application/json")

def authentication_error():
	return HttpResponse("{'message':'ERROR', 'code': 401", content_type="application/json", status_code=401)

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
	apitoken = 	request.META['HTTP_AUTHORIZATION'].split(' ')[1]
	temporaryUser = temp_account_utils.getAccount(apitoken)

	if (temporaryUser != None):
		temp_account_utils.saveData(temporaryUser, request.body)
		return ok_message()
	else:
		return authentication_error()

