from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Invitation
import json
from django.http import HttpResponse
from datetime import datetime
# Create your views here.
ERROR_USERNAME_EXISTS = 5000
ERROR_INVALID_TOKEN = 4000
def default(request):
	return render(request, 'invite_registration.html')


def validate_new_username(request):
	new_username=request.POST['username']
	users = User.objects.filter(username=new_username)
	if (len(users) == 0):
		returnValue = {"message":"OK"}
	else:
		returnValue = {"message":"Username already exists", "error":ERROR_USERNAME_EXISTS}
	return HttpResponse(json.dumps(returnValue), content_type="application/json")


def validate_invitation_token(request):
	try:
		invitation = Invitation.objects.get(token=request.POST['invitation_token'])
	except:
		returnValue = {'message':'Invalid token', 'error':ERROR_INVALID_TOKEN}
		return HttpResponse(json.dumps(returnValue), content_type="application/json")

	if (invitation.numberOfInvitesTaken >= invitation.numberOfInvitesAllowed):
		returnValue = {'message':'This token has expired', 'error':ERROR_INVALID_TOKEN}
		return HttpResponse(json.dumps(returnValue), content_type="application/json")
	
	dateNow = datetime.now().replace(tzinfo=None)
	expiresDate = invitation.expiresDate.replace(tzinfo=None)

	if (expiresDate < dateNow):
		returnValue = {'message':'This token has expired', 'error':ERROR_INVALID_TOKEN}
		return HttpResponse(json.dumps(returnValue), content_type="application/json")

	returnValue = {"message":"OK"}
	return HttpResponse(json.dumps(returnValue), content_type="application/json")

def validate_email(request):
	email = request.POST['email']
	isEmailValid = emailValidation(email)
	users = User.objects.filter(email=email)
	if (len(users) > 0):
		returnValue = {"message":"This email is already registered."}
	else:
		returnValue = {"message":"OK"}
	return HttpResponse(json.dumps(returnValue), content_type="application/json")


def validate_password(request):
	password = request.POST['password']
	returnValue = checkAppropriatePassword(password)
	return HttpResponse(json.dumps(returnValue), content_type="application/json")


def emailValidation(email):
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email( email )
		return True
	except ValidationError:
		return False


def checkAppropriatePassword(password):
	if (len(password) < 8):
		returnValue = {"message":"Password must be at least 8 characters long"}
	else:
		returnValue = {"message":"OK"}
	return returnValue