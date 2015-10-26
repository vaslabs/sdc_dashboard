"""SDC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from sdc_dashboard import views
from email_manager.views import activate_account

urlpatterns = [
    url(r'^dashboard/', include('sdc_dashboard.urls')),
    url(r'^logbook/', include('sdc_dashboard.logbook_urls')),
    url(r'^invites/', include('sdc_invites.urls')),
    url(r'^$', include('sdc_dashboard.urls')), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login', kwargs={'template_name': 'registration/login.html'}),
    url(r'^account/$', views.account_management, name='account_management'),
    url(r'^change-password/$', 'django.contrib.auth.views.password_change', {'template_name': 'registration/password_change_form.html'}, name="password-change"),
    url(r'^change-password/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'registration/password_change_done.html'}, name="password-change-done"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'template_name': 'registration/logout.html'}),
    url('^', include('django.contrib.auth.urls')),
    url(r'^activate/(?P<token>\w{32})', activate_account, name='activate_account'),
]

urlpatterns += staticfiles_urlpatterns()