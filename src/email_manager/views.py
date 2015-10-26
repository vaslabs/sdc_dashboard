from django.shortcuts import render
from sdc_invites.models import ActivationToken
from sdc_dashboard.views import index
from sdc_dashboard.models import SkyDiver

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
	return index(request)


