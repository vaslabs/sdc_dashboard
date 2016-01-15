from django.conf.urls import url

from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^create_account/', csrf_exempt(views.create_account), name='create_account'),
]