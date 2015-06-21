from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^$', views.user_dashboard, name='dashboard'),
 	url(r'^session', views.get_user_data, name='session'),
]