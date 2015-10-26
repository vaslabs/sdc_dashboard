from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from SDC import settings

def send_registration_email(email, activation_token):
	
	if settings.IS_BETA:
		if (not validateEmailForBeta(email)):
			raise Exception('Invalid beta email');

	mail = EmailMultiAlternatives(
	  subject="Skydiver.Ninja account activation",
	  from_email="Skydiver.Ninja No-reply <no-reply@skydiver.ninja>",
	  to=[email]
	)
	mail.attach_alternative('Activate your account <a href="https://dashboard.skydiver.ninja/activate/' + activation_token + '">here</a>', "text/html")

	mail.send()

def validateEmailForBeta(email):
	email_parts = email.split('@')
	if (len(email_parts) != 2):
		return False
	if (email_parts[1] == 'gmail.com' or email_parts[1] == 'googlemail.com'):
		return True
	return False