from django.shortcuts import render
from .models import SkyDiver, SessionData
# Create your views here.
def index(request):
    return render(request, 'dashboard.html')


def user_dashboard(request):
	current_user = request.user
	if (not current_user.is_authenticated())
		return render(request, 'login.html')
	return render(request, 'dashboard.html')
