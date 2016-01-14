from django.test import TestCase
from Crypto.PublicKey import RSA 
from temp_account_utils import create_temporary_account
# Create your tests here.

class TemporaryAccountTestCase(TestCase):
	


	def setUp(self):
		#self.rsa = RSA.generate(bits, e=65537) 
		#self.public_key = rsa.publickey().exportKey("PEM") 
		

	def test_account_is_created(self):
		#account, token = create_temporary_account(self.public_key)
		#print account
		print "Running"