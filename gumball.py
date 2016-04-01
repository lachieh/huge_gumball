from twython import Twython, TwythonStreamer
import pyotp

APP_KEY = 'QMSndpHKNjnWfzMdfZqkDnc66'
APP_SECRET = 'rX7G8758nbHV0wrOeEvi3D3OKR5AtfTMQUgYbI79At6C3ynWLm'

OAUTH_TOKEN = '14652468-IZRc4nTviFqf3qbo6Lq3lnscPFlN1ICF9nBBhDJWr'
OAUTH_TOKEN_SECRET = 'zRLCxqf1V9iDHcD7NpuBxO4MsrN0Ya31nTSK3GnNYkFUV'

search_term = '#ignorethistweetitsatest'

totp = pyotp.TOTP('base32secret3232')
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def CheckFollow(screenname):
	friendships = twitter.lookup_friendships(screen_name=screenname)
	if 'followed_by' in friendships[0]['connections']:
		result = True
	else:
		result = False
	return result

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
		if 'user' in data:
			print 'Triggered tweet: ', data['text']
			print 'by user ', data['user']['screen_name']
			following = CheckFollow(data['user']['screen_name'])
			if following == True:
				print 'User', data['user']['screen_name'], 'is following you.'
				print 'Current OTP:', totp.now()
				validate = totp.verify(int(input('Enter current OTP: ')))
				if validate == True:
					print 'Validation Success'
				else:
					print 'Validation Failed'
			else:
				print 'User', data['user']['screen_name'], '" is NOT following you.'

    def on_error(self, status_code, data):
        print status_code, data


stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

stream.statuses.filter(track=search_term)