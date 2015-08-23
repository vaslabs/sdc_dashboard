from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^username/$', views.validate_new_username, name='validate_new_username'),
   url(r'^validate_invitation_token/$', views.validate_invitation_token, name='validate_invitation_token'),
   url(r'^email/$', views.validate_email, name='validate_email'),
   url(r'^password/$', views.validate_password, name='validate_password'),
   url(r'^register_user/$', views.register_user, name='register_user'),
   url(r'^$', views.default, name='invites_default'),

]