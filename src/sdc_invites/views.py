from django.shortcuts import render

# Create your views here.

def default(request):
	return render(request, 'invite_registration.html')
