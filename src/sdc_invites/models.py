from django.db import models
from sdc_dashboard.models import SkyDiver
from django.contrib.auth.models import User
import calendar
import json
from datetime import datetime

class Invitation(models.Model):
	skydiver = models.ForeignKey(SkyDiver)
	createdDate = models.DateTimeField("date submitted")
	expiresDate = models.DateTimeField("date expires")
	token = models.CharField(max_length=16, unique=True)
	numberOfInvitesAllowed = models.IntegerField()
	numberOfInvitesTaken = models.IntegerField()
    
	def __str__(self):
		return self.token

class ActivationToken(models.Model):
	token = models.CharField(max_length=32, unique=True)
	user = models.ForeignKey(User)
	createdDate = models.DateTimeField("date created")
	activated = models.BooleanField()
	def save(self):
		if not self.id:
			self.createdDate = datetime.now().replace(tzinfo=None)
			self.activated = False
		super(ActivationToken, self).save()
