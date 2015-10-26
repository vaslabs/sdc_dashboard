from django.shortcuts import render
from sdc_invites.models import ActivationToken
from sdc_dashboard.views import index
from sdc_dashboard.models import SkyDiver
from rest_framework.authtoken.models import Token
def activate_account(request, token):
	activationToken = ActivationToken.objects.get(token=token)
	if (activationToken.activated):
		return index(request)
	activationToken.activated = True
	activationToken.save()

	username = activationToken.user.username
	name = username
	skydiver = SkyDiver(username=username, name=name)
	skydiver.save()
	apiToken = Token(user=activationToken.user)
	apiToken.save()
	return index(request)


