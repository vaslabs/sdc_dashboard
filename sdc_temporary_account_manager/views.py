# Create your views here.

from django.shortcuts import render
import json, string, random
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .temp_account_utils import create_temporary_account, encrypt

@csrf_exempt
def create_account(request):
	received_json_data=json.loads(request.body)
	publicKey = received_json_data(received_json_data["publicKey"])
	account, token = create_temporary_account
	encrypted_token = encrypt(account, token)
	response = {}
	response['apitoken'] = encrypted_token
	body = json.dumps(response)
	return HttpResponse(body, content_type="application/json")




