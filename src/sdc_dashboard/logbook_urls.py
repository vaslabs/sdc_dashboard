from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^save/$', views.save_logbook, name='logbook_save'),
    url(r'^api_get/$', views.get_logbook_entries, name='logbook_api_get'),
]