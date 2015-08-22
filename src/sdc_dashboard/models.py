from django.db import models
import calendar
import json

# Create your models here.
class SkyDiver(models.Model):
    username=models.CharField(max_length=50, unique=True)
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.username
    
class SessionData(models.Model):
    skyDiver = models.ForeignKey(SkyDiver)
    submittedDate = models.DateTimeField("date submitted")
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.location

class ShareLink(models.Model):
    shareLink = models.CharField(max_length=16, unique=True)
    userShared = models.ForeignKey(SkyDiver)
    expires = models.DateTimeField("date expires")

    def __str__(self):
        return "/shared_session/" + self.shareLink

class Location(models.Model):
    latitude = models.DecimalField(max_digits=12, decimal_places=9)
    longitude = models.DecimalField(max_digits=12, decimal_places=9)
    name = models.CharField(max_length=255)

class Logbook(models.Model):
    skyDiver = models.ForeignKey(SkyDiver)
    sessionData = models.ForeignKey(SessionData)
    location = models.ForeignKey(Location)

    freeFallTime = models.FloatField()
    exitAltitude = models.FloatField()
    deploymentAltitude = models.FloatField()
    maxVerticalVelocity = models.FloatField()
    date = models.DateTimeField("date of session")
    notes = models.CharField(max_length=1024)

    def __str__(self):
        json_signature = {'id':self.id,\
                            'metrics':{\
                                'freefalltime':self.freeFallTime,\
                                'exitAltitude':self.exitAltitude,\
                                'deploymentAltitude':self.deploymentAltitude,\
                                'maxVelocity':self.maxVerticalVelocity,\
                            },\
                            'timeInMillis':calendar.timegm(self.date.timetuple())*1000,
                            'latitude':str(self.location.latitude),
                            'longitude':str(self.location.longitude),
                            'location':self.location.name,
                            'notes':self.notes
                         }
        return json.dumps(json_signature)