"""
Created by Diandra Kubo and Artur Pimentel
CSE 40437/60437 - Social Sensing and Cyber-Physical Systems 
Spring 2016
University of Notre Dame
Project
Collecting the data
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tweepy.utils import import_simplejson
json = import_simplejson()

# Please assign your keys strings to the variables below
# Consumer keys
consumer_key = "brJuLeztTTpno1Hz1Ni8Q4Q32"
consumer_secret = "8IQYpmH5uAnSNpwZCQEdcBZNCbtinGTwXOV6fh0F3J5J6Ph9x9"

# Access keys
access_token="4870188693-nwxEmTrGC4WKAgzXCgxXbAEHfMOB5we4er8441S"
access_token_secret="wfxWgX8ooHZy5W2ud5Bu7LeC2euhw9IgeoeH3PEvg0DCA"

lon = 0
lat = 1

longitude_left_point = -86.33
latitude_left_point = 41.63
longitude_right_point = -86.20
latitude_right_point = 41.74

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
					#print str(self.n_good_tweets) + ". " + text.encode("utf-8")
					print raw_data
					self.n_good_tweets += 1
					return True
				else:
					return False
		else:
			return True
		

	def on_error(self, status):
		print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    filter_track = ['Zika', 'fever', 'joint pain', 'microcephaly', 'microcefalia', 'mosquitoes', 'mosquito', 'Aedes aegypti', 'mosquito', 'dengue', 'febre', 'fiebre', 'rash', 'muscle pain', 'dor no corpo', 'dolor en el cuerpo', 'dor nas juntas', 'red eyes', 'olho vermelho']

    stream = Stream(auth, l)
    stream.filter(track = filter_track)
