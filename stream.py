from twython import Twython, TwythonStreamer

APP_KEY = 'OXTF145y8NGgzdWsTgQgc2eO4'
APP_SECRET = 'ngjWEGkuHJVv314dUHb1dy8uEvvMxdMOF3XGVAR8K2xG619U4D'

OAUTH_TOKEN = '14652468-74nWSyPTov403RuTPVPEvbyCa5gwUPqn3ColI2q8u'
OAUTH_TOKEN_SECRET = 'dJf9uwD5f7P8PSVauaZHDmogwdk89uqvjKuKDFO5FEZSU'

user = "gumballtester"
text = "test"

class UserStreamer(TwythonStreamer):
	def on_success(self, data):
		if 'direct_message' in data:
			if data['direct_message']['sender']['screen_name'] == user:
				if data['direct_message']['text'] == text:
					print "correct!"

	def on_error(self, status_code, data):
		print status_code, data


stream = UserStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.user()