
from .models import TemporarySkydiver, TemporaryToken
import md5
from Crypto.PublicKey import RSA
from Crypto.Util import asn1
from base64 import b64decode, b64encode

def create_temporary_account(publicKey):
	temporarySkydiver = TemporarySkydiver(publicKey=publicKey)
	temporarySkydiver.save()
	m = md5.new()
	m.update(publicKey)
	print temporarySkydiver.createdDate
	m.update(str(temporarySkydiver.createdDate))
	apiToken = m.hexdigest()
	temporaryApiToken = TemporaryToken(token=apiToken, skydiver=temporarySkydiver)
	temporaryApiToken.save()
	return temporarySkydiver, temporaryApiToken

def encrypt(account, data):
	key = account.publicKey
	publicKeyObj = generatePublicKey(key)
	encrypted_data = publicKeyObj.encrypt(data, 123)
	return b64encode(encrypted_data[0])


def generatePublicKey(key64):
	keyDER = b64decode(key64)
	seq = asn1.DerSequence()
	seq.decode(keyDER)
	keyPub = RSA.construct( (seq[0], seq[1]) )
	return keyPub