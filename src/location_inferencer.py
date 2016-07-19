import googlemaps
import json
import time

from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterError
from datetime import datetime
from pprint import pprint
from pprint import pformat

def get_googlemaps_keys(file_path):
	with open(file_path) as keys_file:
		keys = keys_file.readlines()
		keys = [x.strip('\n') for x in keys]
		return keys

def get_twitter_keys(file_path):
	with open(file_path) as twitter_keys_f:
		twitter_keys_s = twitter_keys_f.read()
		return json.loads(twitter_keys_s)

def most_common(lst):
	return max(set(lst), key=lst.count)

if __name__ == '__main__':
	# Prepare APIs
	gmaps_keys = get_googlemaps_keys('../apikeys/googlemaps_keys.txt')
	gmaps_keys_idx = 0
	gmaps = googlemaps.Client(key=gmaps_keys[gmaps_keys_idx])
	
	twitter_keys = get_twitter_keys("../apikeys/twitter_keys.json")
	twitter = TwitterAPI(twitter_keys['consumer_key'],
					 twitter_keys['consumer_secret'],
					 twitter_keys['access_token'],
					 twitter_keys['access_token_secret'])

	# Set control variable
	SLEEP_TIME = 900 # (seconds) Twitter rates renew every 15 minutes

	with open('../data/dataset_samples/geotag_tweets3.json') as dataset_f, \
		 open('../data/loc_results/gt_cities2.txt', 'w') as gt_locs_f, \
		 open('../data/logs/loc_infer_log.txt', 'a') as log:

		for i, line in enumerate(dataset_f):
			tweet = json.loads(line)

			# First, translate coordinates from tweet to the city where it belongs
			got_reverse_geocode = False
			while not got_reverse_geocode:
				try:
					reverse_geocode_result = gmaps.reverse_geocode(tuple(tweet['coordinates']['coordinates'])[::-1])
					got_reverse_geocode = True
				except:
					# If that key expired, try this one. Limit is 2400 requests per day per key for gmaps
					gmaps_keys_idx += 1
					gmaps = googlemaps.Client(key=gmaps_keys[gmaps_keys_idx])

			# Retrieve city name from google maps response
			username = tweet['user']['screen_name'].encode('utf-8')
			if reverse_geocode_result != None:
				has_city = False
				# Find the place in the list that has the city information
				for place in reverse_geocode_result:
					place_type = place['address_components'][0]['types']
					if cmp(place_type, [u'locality', u'political']) == 0:
						geocode_r_str = place['address_components'][0]['short_name'].encode('utf-8')
						has_city = True
				if has_city == False:
					geocode_r_str = "NO_CITY"
			else:
				geocode_r_str = "NO_RESULT"

			# Request friends ids
			got_friends = False
			friends_ids = ""
			while not got_friends:
				try:
					friends_r = twitter.request('friends/ids',
						{'count':100, 'screen_name': tweet['user']['screen_name']})
					got_friends = True
				except TwitterError.TwitterRequestError:
					print "Trying next friends request in 15 minutes\n"
					log.write("Trying next friends request in 15 minutes\n")
					time.sleep(SLEEP_TIME)
			# Prepare a list of friends ids from the response
			try:
				friends = set(friends_r.response.json()["ids"])
			except KeyError:
				print "Trying next friends iterator request in 15 minutes\n"
				log.write("Trying next friends iterator request in 15 minutes\n")
				time.sleep(SLEEP_TIME)
				continue

			# Request followers ids
			got_followers = False
			while not got_followers:
				try:
					followers_r = twitter.request('followers/ids',
						{'count':1000, 'screen_name':tweet['user']['screen_name']})
					got_followers = True
				except TwitterError.TwitterRequestError:
					print "Trying next followers request in 15 minutes\n"
					log.write("Trying next followers request in 15 minutes\n")
					time.sleep(SLEEP_TIME)
			# Prepare a list of followers ids from the response
			try:
				followers = set(followers_r.response.json()["ids"])
			except KeyError:
				print "Trying next followers iterator request in 15 minutes\n"
				log.write("Trying next followers iterator request in 15 minutes\n")
				time.sleep(SLEEP_TIME)
				continue

			# Get a list with bi-directed connections
			connections = friends.intersection(followers)
			connections_ids = ""
			for connection in connections:
				connections_ids += "," + str(connection)

			# Get the locations of those connections
			connections_locations = []
			got_users = False
			while not got_users:
				try:
					users_r = twitter.request('users/lookup', {'user_id': connections_ids[1:]})
					got_users = True
				except TwitterError.TwitterRequestError:
					print "Trying next users request in 15 minutes\n"
					log.write("Trying next users request in 15 minutes\n")
					time.sleep(SLEEP_TIME)

			for item in users_r.response.json():
				if 'location' in item:
					if item['location'] != "":
						# First substring before a comma usually is a city
						connections_locations.append(item['location'].split(",")[0])

			inference_r_str = most_common(connections_locations).encode('utf-8') + "\n"

			gt_locs_f.write(username + "," + geocode_r_str + ","  + inference_r_str + "\n")
			print username + "," + geocode_r_str + ","  + inference_r_str