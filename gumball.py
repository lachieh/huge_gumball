from twython import Twython, TwythonStreamer
from twitter_auth import *
import pyotp

search_term = '#ignorethistweetitsatest'

totp = pyotp.TOTP('base32secret3232')
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
current_user = ""

def CheckFollow(screenname):
	friendships = twitter.lookup_friendships(screen_name=screenname)
	if 'followed_by' in friendships[0]['connections']:
		result = True
	else:
		result = False
	return result


def CheckPassWithUser(user_screen_name):
	message_text = "Thanks! What's the current OTP?"
	twitter.send_direct_message(screen_name=user_screen_name, text=message_text)
	print "DM sent to user ", user_screen_name
	stream = UserStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	global current_user
	current_user = user_screen_name
	stream.user()

class UserStreamer(TwythonStreamer):
	def on_success(self, data):
		print 'Current OTP:', totp.now()
		if 'direct_message' in data:
			if data['direct_message']['sender']['screen_name'] == current_user:
				validate = totp.verify(int(data['direct_message']['text']))
				print validate
				if validate == True:
					print 'Authentication Passed'
					self.disconnect()
				else:
					print 'Failed Authentication. Waiting...'

	def on_error(self, status_code, data):
		print status_code, data

class SearchStreamer(TwythonStreamer):
    def on_success(self, data):
		if 'user' in data:
			print 'Triggered tweet: "', data['text'],'" by user', data['user']['screen_name']
			following = CheckFollow(data['user']['screen_name'])
			if following == True:
				print 'User', data['user']['screen_name'], 'is following you.'
				CheckPassWithUser(data['user']['screen_name'])
			else:
				print 'User', data['user']['screen_name'], '" is NOT following you.'

    def on_error(self, status_code, data):
        print status_code, data


stream = SearchStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

stream.statuses.filter(track=search_term)