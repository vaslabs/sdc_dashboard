
from .models import TemporarySkydiver, TemporaryToken, TemporarySessionData
import md5
from Crypto.PublicKey import RSA
from Crypto.Util import asn1
from base64 import b64decode, b64encode, urlsafe_b64decode
import random
import datetime
from SDC import settings
import json
from sdc_dashboard.sdc_utils import logbookRawData

SESSION_LIMIT = 5

def create_temporary_account(publicKey):
	temporarySkydiver = TemporarySkydiver.objects.filter(publicKey=publicKey)
	if (len(temporarySkydiver) > 0):
		temporarySkydiver = temporarySkydiver[0]
		temporaryApiToken = TemporaryToken.objects.filter(skydiver=temporarySkydiver)
		if (len(temporaryApiToken) == 0):
			temporaryApiToken = createToken(publicKey, temporarySkydiver)
		else:
			temporaryApiToken = temporaryApiToken[0]
		return temporarySkydiver, temporaryApiToken
	temporarySkydiver = TemporarySkydiver(publicKey=publicKey)
	temporarySkydiver.save()
	
	apiToken = createToken(publicKey, temporarySkydiver)
	temporaryApiToken = TemporaryToken(token=apiToken, skydiver=temporarySkydiver)
	temporaryApiToken.save()
	return temporarySkydiver, temporaryApiToken

def createToken(publicKey, temporarySkydiver):
	m = md5.new()
	m.update(publicKey)
	m.update(str(temporarySkydiver.createdDate))
	return m.hexdigest()

def encrypt(account, data):
	key = account.publicKey
	publicKeyObj = generatePublicKey(key)
	print 'Data:', data
	encrypted_data = publicKeyObj.encrypt(str(data), 123)
	return b64encode(encrypted_data[0])


def generatePublicKey(key64):
	key='-----BEGIN PUBLIC KEY-----\n'+\
		key64 +\
		'\n-----BEGIN PUBLIC KEY-----'
	return RSA.importKey(key)

def getAccount(apitoken):
	tokenObject = TemporaryToken.objects.get(token=apitoken)
	if tokenObject == None:
		return None
	account = tokenObject.skydiver
	return account

def saveData(account, data):
	
	if (account.sessionsSubmitted >= SESSION_LIMIT):
		raise LimitPassedError(account.sessionsSubmitted)
	date_submitted = datetime.datetime.now()
	file_name = str(random.randint(0, 1000000)) + str(date_submitted.time()) + '.json'
	data_file = open(settings.DATA_DIR + "/" + file_name, 'w')
	data_file.write(data)
	data_file.close()
	
	sessionData = TemporarySessionData(temporarySkydiver=account, location = file_name)
	sessionData.save()
	account.sessionsSubmitted += 1
	account.save()

def getSessions(account):
	return TemporarySessionData.objects.filter(temporarySkydiver=account)

def getSession(account, sessionId):
	session=TemporarySessionData.objects.get(id=sessionId, temporarySkydiver=account)
	return logbookRawData(session)


class LimitPassedError(Exception):

	def __init__(self, sessionsDone):
		Exception.__init__()
		self.sessions = sessionsDone

	def __str__(self):
		return "You passed the limit of your temporary account: " + str(self.sessions) + ". Create an account to continue using the app"