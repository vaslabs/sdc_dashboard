from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Invitation, ActivationToken
import json
from django.http import HttpResponse
from datetime import datetime
from email_manager.utils import send_registration_email
# Create your views here.
ERROR_USERNAME_EXISTS = 5000
ERROR_INVALID_TOKEN = 4000
def default(request):
	return render(request, 'invite_registration.html')


def validate_new_username(request):
	new_username=request.POST['username']
	returnValue = validateUsername(new_username)
	return HttpResponse(json.dumps(returnValue), content_type="application/json")


def validate_invitation_token(request):
	token = request.POST['invitation_token']
	returnValue = validateToken(token)
	return HttpResponse(json.dumps(returnValue), content_type="application/json")

def validate_email(request):
	email = request.POST['email']
	returnValue = emailValidation(email)
	return HttpResponse(json.dumps(returnValue), content_type="application/json")


def validate_password(request):
	password = request.POST['password']
	returnValue = checkAppropriatePassword(password)
	return HttpResponse(json.dumps(returnValue), content_type="application/json")


def email_validation(email):
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email( email )
		return True
	except ValidationError:
		return False

def validateUsername(username):
	if(len(username) < 5):
		return {'message':"Username must be at least 5 characters long"}
	users = User.objects.filter(username=username)
	if (len(users) == 0):
		returnValue = {"message":"OK"}
	else:
		returnValue = {"message":"Username already exists", "error":ERROR_USERNAME_EXISTS}
	return returnValue
def checkAppropriatePassword(password):
	if (len(password) < 8):
		returnValue = {"message":"Password must be at least 8 characters long"}
	else:
		returnValue = {"message":"OK"}
	return returnValue

def emailValidation(email):
	isEmailValid = email_validation(email)
	if (not isEmailValid):
		return {"message":"Not a valid email address"}
	users = User.objects.filter(email=email)
	if (len(users) > 0):
		returnValue = {"message":"This email is already registered."}
	else:
		returnValue = {"message":"OK"}
	return returnValue

def validateToken(token):
	try:
		invitation = Invitation.objects.get(token=token)
	except:
		return {'message':'Invalid token', 'error':ERROR_INVALID_TOKEN}

	if (invitation.numberOfInvitesTaken >= invitation.numberOfInvitesAllowed):
		return {'message':'This token has expired', 'error':ERROR_INVALID_TOKEN}
	
	dateNow = datetime.now().replace(tzinfo=None)
	expiresDate = invitation.expiresDate.replace(tzinfo=None)

	if (expiresDate < dateNow):
		return {'message':'This token has expired', 'error':ERROR_INVALID_TOKEN}

	return {"message":"OK"}

def register_user(request):
	
	username = request.POST['username']
	usernameResponse = validateUsername(username)
	if (usernameResponse['message'] != 'OK'):
		return HttpResponse(json.dumps(usernameResponse), content_type="application/json")
	
	password = request.POST['password']
	passwordResponse = checkAppropriatePassword(password)
	if (passwordResponse['message'] != 'OK'):
		return HttpResponse(json.dumps(passwordResponse), content_type="application/json")

	email = request.POST['email']
	emailResponse = emailValidation(email)
	if (emailResponse['message'] != 'OK'):
		return HttpResponse(json.dumps(emailResponse), content_type="application/json")

	token = request.POST['invitation_token']
	tokenResponse = validateToken(token)
	if (tokenResponse['message'] != 'OK'):
		return HttpResponse(json.dumps(tokenResponse), content_type="application/json")

	try:
		user = User.objects.create_user(username, email, password)
		user.save()
		returnValue = {"message":"OK"}
		invitation = Invitation.objects.get(token=token)
		invitation.numberOfInvitesTaken = invitation.numberOfInvitesTaken + 1
		invitation.save()
		activationToken = createActivationToken(username, email, user)
		activationToken.save()
		send_registration_email(email, activationToken.token)
	except Exception as e:
		print e
		returnValue = {"message":"Failed to register. Please contact vaslabsco@gmail.com"}

	return HttpResponse(json.dumps(returnValue), content_type="application/json")


import md5
def createActivationToken(username, email, user):
	m = md5.new()
	m.update(username)
	m.update(email)
	return ActivationToken(token=m.hexdigest(), user=user)