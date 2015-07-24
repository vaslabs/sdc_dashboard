from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logbook/(\d+)/$', views.user_dashboard, name='logbook_dashboard'),
    url(r'^$', views.user_dashboard, name='dashboard'),
    url(r'^sessions$', views.get_user_sessions, name='sessions'),
    url(r'^logbook$', views.get_logbook_screen, name='logbook'),
 	url(r'^session$', views.get_user_data, name='session'),
    url(r'^session/(?P<sessionNo>\d)$', views.get_user_data, name='sp_session'),
 	url(r'^graphs$', views.load_user_graphs, name='graphs'),
    url(r'^share$', views.share_latest_dive, name='session_share'),
    url(r'^shared_session/(?P<linkid>\w{16})', views.get_shared_session, name='shared_session'),
    url(r'^shared_session/l/(?P<linkid>\w{16})', views.view_shared_session, name='view_shared_session'),
    url(r'^submit$', views.save_session_data, name='save_session_data'),
    url(r'^apitoken$', views.get_api_token, name='api_token'),
    url(r'^apiqr$', views.get_qrcode_api, name='api_qr'),
    url(r'^demo$', views.get_demo_page, name='demo_page'),
    url(r'^demodata$', views.get_demo_data, name='demo_data'),
]