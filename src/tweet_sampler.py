"""
Zikafinder 1.01
Created by Artur Pimentel
Summer 2016 - University of Notre Dame
Collecting the data
"""
import os
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.utils import import_simplejson

###############################################################################
json = import_simplejson()

###############################################################################
class StdOutListener(StreamListener):
	n_good_tweets = 0
	n_total_tweets = 0
	symptoms_keywords = []
	vector_keywords = []

	def def_new_output_from(self, file_path):
		data_dir_list = os.listdir(file_path)

		for i in range(len(data_dir_list) + 1):
			new_file_name = "crawler_output" + str(i) + ".json"
			if new_file_name not in data_dir_list:
				self.output_f = open(file_path + new_file_name, "w")
				break

	def is_in_both_klists(self, text):
		text = text.lower()
		for skw in self.symptoms_keywords:
			if skw in text:
				for vkw in self.vector_keywords:
					if vkw in text:
						return True
		return False

	def on_data(self, raw_data):

		data = json.loads(raw_data)
		
		if data.has_key("text"):
			text = data["text"]
			if text is None:
				return True
			else:
				if self.n_good_tweets < self.n_total_tweets:
					if self.is_in_both_klists(text):
						self.output_f.write(raw_data)

						self.n_good_tweets += 1
						b = (str(self.n_good_tweets) + "/" + 
							str(self.n_total_tweets) + " tweets collected.")
						sys.stdout.write('\r' + b)
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

###############################################################################
if __name__ == '__main__':

	if len(sys.argv) != 2:
		print "Wrong number of args. Command should be:"
		print "python tweet_sampler.py [# of tweets to be collected]"

	elif int(sys.argv[1]) <= 0:
		print "# of tweets to be collected has to be a positive integer value"

	else:
		keys = get_twitter_keys("../apikeys/twitter_keys.json")

		l = StdOutListener()
		l.def_new_output_from("../data/crawler/")
		l.n_total_tweets = int(sys.argv[1])

		auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
		auth.set_access_token(keys['access_token'], 
							  keys['access_token_secret'])

		l.symptoms_keywords = get_keywords("param/crawler_keywords_symptoms.txt")
		l.vector_keywords = get_keywords("param/crawler_keywords_vector.txt")
		filter_track = l.symptoms_keywords + l.vector_keywords
		
		stream = Stream(auth, l)
		stream.filter(track = filter_track)