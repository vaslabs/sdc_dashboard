from __future__ import unicode_literals

from django.db import models

# Create your models here.


class TemporarySkydiver(models.Model):
	publicKey=models.CharField(max_length=512)
	sessionsSubmitted=models.IntegerField(default=0)
	createdDate = models.DateTimeField(auto_now_add=True)


class TemporarySessionData(models.Model):
    temporarySkydiver = models.ForeignKey(TemporarySkydiver)
    submittedDate = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    def __str__(self):
        return self.location


class TemporaryToken(models.Model):
	token=models.CharField(max_length=32, unique=True)
	skydiver=models.ForeignKey(TemporarySkydiver)
	def __str__(self):
		return skydiver.publicKey + ':' + self.token


