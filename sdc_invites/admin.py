from django.contrib import admin
from .models import Invitation, ActivationToken
admin.site.register(Invitation)
admin.site.register(ActivationToken)
# Register your models here.
