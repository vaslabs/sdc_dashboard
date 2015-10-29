from django.contrib import admin
from .models import SessionData, SkyDiver, Logbook
# Register your models here.
admin.site.register(SessionData)
admin.site.register(SkyDiver)
admin.site.register(Logbook)