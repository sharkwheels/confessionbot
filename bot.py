import re
import os

import random
from random import choice

from twython import Twython, TwythonError
from twython import TwythonStreamer



### GET KEYS  #########################################################################

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
twitter.verify_credentials()


### CONFFESSI0NAL BOT ##########################################################

class ConStreamer(TwythonStreamer):

	def on_success(self, data):
		if 'direct_message' in data:
			self.deal_direct(data)
		"""
		elif 'text' in data:
			self.deal_public_response(data)
		"""
		
	def deal_direct(self,data):

		### parse raw data
		msg = data['direct_message']
		#print(msg)
		body = msg['text']
		recepId = msg['recipient_id']
		msgId = msg['id']
		senderName = msg['sender_screen_name']

		tireFire = "You've tripped the twitter tire fire filter! Take out your @ metions / links / pics / slurs and try again. Emojis are cool tho."
		forgot = "You need to start your DM with: ~"

		### controls and stops
		controlID = os.environ['CTRL_ID']
		controlC = '~'
		stopWords = set(['rape','murder','nigger','cunt','fag','homo','@','#','http'])  ## no tire fires, no tagging, no hashtags, no links, no pics
		

		### general logic 
			### refactor this...
		if recepId == controlID and body.startswith(controlC):
			## test for swears and shit
			if not any(w in body for w in stopWords):
				body = re.sub('^~\s','',body)
				b = re.sub('\s+',' ',body)
				try:
					twitter.update_status(status=b)
					print("{0}:{1}".format(recepId,b))
				except TwythonError as e:
					print(e)					
			elif any(w in body for w in stopWords):
				twitter.send_direct_message(screen_name=senderName,text=tireFire)
				print(tireFire)
			else:
				pass

		elif recepId == controlID and not body.startswith(controlC):
			twitter.send_direct_message(screen_name=senderName,text=forgot)
			print(forgot)
			
		else:
			pass
		#twitter.destroy_direct_message(id=msgId)
	
	def get_random(self):
		sayings = [
			"I'm sorry, I don't really deal w/ @ responses.",
			"Check the pinned tweet.",
			"Look at the pinned tweet.",
			"Check out the pinned tweet.",
			"The pinned tweet will tell you how to work this.",
			"I don't work with @ responses.",
			"I don't really work with @ responses.",
			"Try a DM rather than an @ response.",
			"Check out the sidebar or the pinned tweet.",
			"You'll probably want to try a DM.",
			"Void spitters only work with DMs.",
			"The void only listens to your DMs.",
			"Pinned Tweet my friend.",
			"Voids + @ resposes = beep beep beep",
			"Beep beep beep",
			"Bzzzzzzzzzzzzzzzzzzzzzz",
			"Beeeeeeeeeesssssssssss",
			"Merp"
		]
		choice = random.choice(sayings)
		return choice

	def deal_public_response(self,data):
		body = data['text']
		user = data['user']['screen_name']
		acct = "@smlconfessional"
		saying = self.get_random()
		toTweet = "@{0}: {1}".format(user,saying)
		if body.startswith(acct):
			try:
				twitter.update_status(status=toTweet)
				print(toTweet)
			except TwythonError as e:
				print(e)
	

	def on_error(self, status_code, data):
		print(status_code, data)
		self.disconnect()
		


### CALL STREAM ##########################################################

stream = ConStreamer(CONSUMER_KEY, CONSUMER_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.user()

#"DMs are open. DMs must start with a '~' to be posted. Text and emojis are cool. Tire-fires, links, pics, and mentions, are not."
