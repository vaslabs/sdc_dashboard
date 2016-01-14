
from .models import TemporarySkydiver, TemporaryToken
import md5

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