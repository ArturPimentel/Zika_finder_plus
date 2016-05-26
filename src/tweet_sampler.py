"""
Created by Diandra Kubo and Artur Pimentel
CSE 40437/60437 - Social Sensing and Cyber-Physical Systems 
Spring 2016
University of Notre Dame
Project
Collecting the data
"""
import os

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.utils import import_simplejson

###############################################################################
json = import_simplejson()
output_f = ""

###############################################################################
class StdOutListener(StreamListener):
	n_good_tweets = 0

	def on_data(self, raw_data):

		data = json.loads(raw_data)
		
		if data.has_key("text"):
			text = data["text"]
			if text is None:
				return True
			else:
				if self.n_good_tweets < 1000000:
					output_f.write(raw_data)
					self.n_good_tweets += 1
					return True
				else:
					return False
		else:
			return True
		

	def on_error(self, status):
		print status

###############################################################################
def get_twitter_keys(file_path):
	with open(file_path) as twitter_keys_f:
		twitter_keys_s = twitter_keys_f.read()
		return json.loads(twitter_keys_s)

def get_keywords(file_path):
	with open(file_path) as keywords_f:
		keywords = keywords_f.readlines()
		keywords = [x.strip('\n') for x in keywords]
		return keywords

def def_new_output_from(file_path):
	data_dir_list = os.listdir(file_path)

	for i in range(listdir):
		if "crawler_output" + i not in listdir:
			output_f = open("crawler_output" + i, "w")
			break

###############################################################################
if __name__ == '__main__':
	
	keys = get_twitter_keys("../apikeys/twitter_keys.json")
	def_new_output_from("../data/crawler/")

	l = StdOutListener()
	auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	auth.set_access_token(keys['access_token'], keys['access_token_secret'])

	filter_track = get_keywords("param/crawler_keywords.txt")

	stream = Stream(auth, l)
	stream.filter(track = filter_track)
