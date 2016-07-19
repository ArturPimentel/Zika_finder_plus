import googlemaps
import json
import time

from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterError
from datetime import datetime
from pprint import pprint
from pprint import pformat

def get_twitter_keys(file_path):
	with open(file_path) as twitter_keys_f:
		twitter_keys_s = twitter_keys_f.read()
		return json.loads(twitter_keys_s)

def most_common(lst):
	return max(set(lst), key=lst.count)

if __name__ == '__main__':
	# Prepare APIs
	gmaps = googlemaps.Client(key='AIzaSyCndwIGj8tmXEdXGyvMhXvWWhh0iTiqius')
	keys = get_twitter_keys("../apikeys/twitter_keys.json")
	api = TwitterAPI(keys['consumer_key'],
					 keys['consumer_secret'],
					 keys['access_token'],
					 keys['access_token_secret'])

	# Set control variables
	n_locs_inf = 0
	TWITTER_API_LIMIT = 12
	SLEEP_TIME = 900

	with open('../data/dataset_samples/geotag_tweets3.json') as f, \
		 open('../data/loc_results/gt_cities2.txt', 'w') as gt_locs_f, \
		 open('../data/logs/loc_infer_log.txt', 'a') as log:

		for i, line in enumerate(f):
			if i >= n_locs_inf and i < n_locs_inf + TWITTER_API_LIMIT:
				tweet = json.loads(line)

				try:
					reverse_geocode_result = gmaps.reverse_geocode(tuple(tweet['coordinates']['coordinates'])[::-1])
				except:
					gmaps = googlemaps.Client(key='AIzaSyBUU2cnAhQ0vNPqxNpNK_PNwKRW5kxwwbk')
					reverse_geocode_result = gmaps.reverse_geocode(tuple(tweet['coordinates']['coordinates'])[::-1])

				if reverse_geocode_result != None:
					has_city = False
					for place in reverse_geocode_result:
						place_type = place['address_components'][0]['types']
						if cmp(place_type, [u'locality', u'political']) == 0:
							gt_locs_f.write(tweet['user']['screen_name'].encode('utf-8') + "," + place['address_components'][0]['short_name'].encode('utf-8'))
							has_city = True
					if has_city == False:
						gt_locs_f.write(tweet['user']['screen_name'].encode('utf-8') + ",NO_CITY")
				else:
					gt_locs_f.write(tweet['user']['screen_name'].encode('utf-8') + ",NO_RESULT")

				got_friends = False
				friends_ids = ""
				while not got_friends:
					try:
						friends_r = api.request('friends/ids', {'count':100, 'screen_name': tweet['user']['screen_name']})
						got_friends = True
					except TwitterError.TwitterRequestError:
						print "Trying next friends request in 15 minutes\n"
						log.write("Trying next friends request in 15 minutes\n")
						time.sleep(SLEEP_TIME)

				got_followers = False
				while not got_followers:
					try:
						followers_r = api.request('followers/ids', {'count':1000, 'screen_name':tweet['user']['screen_name']})
						got_followers = True
					except TwitterError.TwitterRequestError:
						print "Trying next followers request in 15 minutes\n"
						log.write("Trying next followers request in 15 minutes\n")
						time.sleep(SLEEP_TIME)

				print friends_r, followers_r
				try:
					friends = set(friends_r.response.json()["ids"])
				except KeyError:
					print "Trying next friends iterator request in 15 minutes\n"
					log.write("Trying next friends iterator request in 15 minutes\n")
					time.sleep(SLEEP_TIME)
					continue

				try:
					followers = set(followers_r.response.json()["ids"])
				except KeyError:
					print "Trying next followers iterator request in 15 minutes\n"
					log.write("Trying next followers iterator request in 15 minutes\n")
					time.sleep(SLEEP_TIME)
					continue


				connections = friends.intersection(followers)
				connections_ids = ""
				for connection in connections:
					connections_ids += "," + str(connection)

				connections_locations = []
				r = api.request('users/lookup', {'user_id': connections_ids[1:]})
				for item in r.get_iterator():
					if 'location' in item:
						if item['location'] != "":
							connections_locations.append(item['location'].split(",")[0])

				gt_locs_f.write("," + most_common(connections_locations).encode('utf-8') + "\n")
				n_locs_inf += 1
			else:
				print "Trying next general request in 15 minutes\n"
				log.write("Trying next general request in 15 minutes\n")
				n_locs_inf += TWITTER_API_LIMIT
				time.sleep(SLEEP_TIME)