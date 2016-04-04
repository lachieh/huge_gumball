from twython import Twython, TwythonStreamer
from twitter_auth import *
from RpiLcdBackpack import AdafruitLcd
import pyotp

search_term = '#ignorethistweet'

totp = pyotp.TOTP('hugeprizemachine')
lcd = AdafruitLcd()
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
	message_text = "Thanks for sharing! Enter the current OTP on the screen to claim your prize!"
	twitter.send_direct_message(screen_name=user_screen_name, text=message_text)
	print "DM sent to user ", user_screen_name
	stream = UserStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	global current_user
	current_user = user_screen_name
	stream.user()

def ScreenOn():
	lcd.backlight(True)
	lcd.cursor(False)
	lcd.blink(False)

def ScreenOff():
	lcd.clear()
	lcd.backlight(False)

def ClearAndPrint(message):
	lcd.clear()
	lcd.message(message)

class UserStreamer(TwythonStreamer):
	def on_success(self, data):
		message = "Thanks for tweeting!\2Please reply with\3these numbers:\4       " + totp.now()
		ScreenOn()
		ClearAndPrint(message)
		if 'direct_message' in data:
			if data['direct_message']['sender']['screen_name'] == current_user:
				max_errors = 3
				if max_errors:
					validate = totp.verify(int(data['direct_message']['text']))
					print validate
					if validate == True:
						message = "Correct Code!\2Dispensing Now..."
						ClearAndPrint(message)
						print 'Authentication Passed'
						self.disconnect()
						time.sleep(10)
						ScreenOff()
					else:
						max_errors -= 1
						print 'Authentication Failed. Try again...'
				else:
					print "Authentication Failed 3 times. Exiting."
					self.disconnect()
					ScreenOff()

	def on_error(self, status_code, data):
		print status_code, data

class SearchStreamer(TwythonStreamer):
    def on_success(self, data):
		if 'user' in data:
			print 'Triggered tweet: "' + data['text'] + '" by user' + data['user']['screen_name']
			following = CheckFollow(data['user']['screen_name'])
			if following == True:
				print 'User', data['user']['screen_name'], 'is following you.'
				CheckPassWithUser(data['user']['screen_name'])
			else:
				print 'User', data['user']['screen_name'], '" is NOT following you.'

    def on_error(self, status_code, data):
        print status_code, data

stream = SearchStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

print 'Listening for tweets containing the term:"' + search_term + '"'
stream.statuses.filter(track=search_term)
