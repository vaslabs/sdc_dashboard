from django.db import models
from sdc_dashboard.models import SkyDiver
import calendar
import json

class Invitation(models.Model):
	skydiver = models.ForeignKey(SkyDiver)
	createdDate = models.DateTimeField("date submitted")
	expiresDate = models.DateTimeField("date expires")
	token = models.CharField(max_length=16, unique=True)
	numberOfInvitesAllowed = models.IntegerField()
	numberOfInvitesTaken = models.IntegerField()
    
	def __str__(self):
		return self.token