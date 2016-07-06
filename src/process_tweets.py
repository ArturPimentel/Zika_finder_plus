"""
Zikafinder 1.01
Created by Diandra Kubo as process_tweets.py
Modified by Artur Pimentel
Summer 2016 - University of Notre Dame
Extract Locations from tweets and separate the relevant fields
"""

import numpy as np
import json
import sys
import os.path
import datetime

from place import Place
from fixLocations import LocationFinder
from datetime import datetime

###############################################################################
class Process():
	"""
	Input file should be a list of the relevant tweet JSONs
	Directory is the directory where the tweets are. For this project, I'm 
	maintaining the tweets in the "../data/dataset_samples" directory
	"""
	def __init__(self, input_file,  directory):
		self.input_file = input_file
		self.directory = directory
		self.coding = 'utf-8'

		# create a list of tweets
		self.load_tweets()
		# process this list of tweets
		self.process()
	
	# make unicode string ASCII	
	def deformat(self, s):
		return s.decode(self.coding)
	
	# make ASCII string unicode	
	def format(self, s):
		return s.encode(self.coding)

	# Check if the tweet is an error message (e.g. 401, 406)
	def isTweetError(self, tweet):
		return len(tweet) < 3

	# Reads tweets from the input file and save them into self.tweets
	def load_tweets(self):
		f = open(self.directory + self.input_file, "r")
		
		self.tweets = []

		for line in f: 
			if line != '\n' and not self.isTweetError(line):
				try:
					t = json.loads(line)
				except:
					# DEBUG
					sys.stdout.write("'" + line + "'")
					print len(line)
					sys.exit()
				self.tweets.append(t)		
		return
	
	# Parse and read a file of known locations, storing them in a list
	def load_known_locations(self, filename):
		known_locations = []

		with open(filename, 'r') as f:
			for line in f:
				# Each line in the locations file is in the form
				# [latitude], [longitude], "[place]"
				# Example:
				# 10.4805937,-66.9036063,"Caracas, Venezuela"
				parsed_line = line.split('"')

				known_locations.append(Place(self.deformat(parsed_line[1]),
											 parsed_line[0].split(",")[0],
											 parsed_line[0].split(",")[1]))

		return known_locations

	# Take the latitute and longitude from the center of the bounding box
	def get_tweet_latitude(self, tweet):
		return ((
					float(tweet['place']['bounding_box']['coordinates'][0][0][1]) +
					float(tweet['place']['bounding_box']['coordinates'][0][2][1])
				) / 2)

	def get_tweet_longitude(self, tweet):
		return (( 
					float(tweet['place']['bounding_box']['coordinates'][0][0][0]) +
					float(tweet['place']['bounding_box']['coordinates'][0][2][0]) 
				) / 2)

	def is_location_known(self, user_location):
		return (x in tuple(known_locations_names)) == True

	def write_csv(self):
		# Write csv file with all the treated tweets
		with open("../data/csv/" + self.input_file.split(".")[0] + ".csv", "w") as output:
			output.write("tweet_id|user_id|latitude|longitude|language|loc_type|send_time|text")
			for tweet in self.treated_tweets:
				output.write("\n" + str(tweet['tweet_id']) + "|" +
							 str(tweet['user_id']) + "|" +
							 str(tweet['latitude']) + "|" +
							 str(tweet['longitude']) + "|" +
							 tweet['language'] + "|" +
							 tweet['loc_type'] + "|")
				output.write(tweet['send_time'])
				output.write("|\"")
				output.write(self.format(tweet['text']).replace("\n", "\\n").replace("\"", "'"))
				output.write("\"")

	def write_log(self, n_new_userloc_tweets, n_old_userloc_tweets, n_geotag_tweets, n_loc_tweets):
		# Write log with tweet statistics
		with open("../data/logs/process_tweets_log.txt", "a") as log:
			log.write("---------------------------------------------------------\n")
			log.write('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.now()) + "\n")
			log.write(str(n_new_userloc_tweets) + " non-processed user locations\n")
			log.write(str(n_old_userloc_tweets) + " processed user locations\n")
			log.write(str(n_geotag_tweets) + " are geotagged tweets\n")
			log.write(str(n_loc_tweets) + " of " + str(len(self.tweets)) + 
					" had location. " + str(float(n_loc_tweets)/float(len(self.tweets))*100) + 
					"%\n")

	def process(self):
		# List with the only necessary fields of a tweet
		self.treated_tweets = []
		# List with the locations geolocated before
		known_locations = []
		# Counters for log statistics
		n_loc_tweets = 0; n_geotag_tweets = 0; n_old_userloc_tweets = 0; n_new_userloc_tweets = 0

		# Load list of known locations
		filename = 'param/addresses_newkeywords.txt'
		if os.path.isfile(filename):
			known_locations = self.load_known_locations(filename)
		known_locations_names = [self.format(kl.name) for kl in known_locations]

		# Prepare tweet list
		with open(filename, 'a') as city_coordinates_f:
			loc_finder = LocationFinder()

			for tweet in self.tweets:
				# Fill the first fields of each tweet
				treated_tweet = {}
				treated_tweet['tweet_id'] = tweet['id']
				treated_tweet['user_id'] = tweet['user']['id']
				treated_tweet['send_time'] = tweet['created_at']
				treated_tweet['text'] = tweet['text']
				treated_tweet['language'] = tweet['lang']
				
				# Find or infer where the tweet was sent
				# if the tweet is geotagged
				if tweet['place'] != None:
					treated_tweet['longitude'] = self.get_tweet_longitude(tweet)
					treated_tweet['latitude'] = self.get_tweet_latitude(tweet)
					treated_tweet['loc_type'] = 'Geotag'
					n_geotag_tweets += 1
					n_loc_tweets += 1

					self.treated_tweets.append(treated_tweet)
				# if the tweet is not geotagged, but the user profile provides a city of origin
				elif tweet['user']['location'] != None:
					user_location = self.format(tweet['user']['location'])
					if user_location not in known_locations_names:
						# Use FixLocations to find city's coordinates
						loc = loc_finder.find_location_coordinates(user_location)

						# If it wasn't successful, consider as type 3
						if loc == None:
							#Use type 3 method for inferring location, for now, don't append to the list and continue loop
							continue
						# Otherwise, write location to the known locations file
						else:
							treated_tweet['longitude'] = loc.longitude
							treated_tweet['latitude'] = loc.latitude
							city_coordinates_f.write("%s,%s,\"%s\"\n" % 
													(loc.latitude, loc.longitude, loc.name))
							n_new_userloc_tweets += 1
					else:
						index = known_locations_names.index(user_location)
						treated_tweet['longitude'] = known_locations[index].longitude
						treated_tweet['latitude'] = known_locations[index].latitude
						n_old_userloc_tweets+=1
		 			
		 			treated_tweet['loc_type'] = 'User profile'
					self.treated_tweets.append(treated_tweet)
					n_loc_tweets += 1
				else:
					# Use a method of inferring the tweet location
					pass

		write_csv()
		write_log(n_new_userloc_tweets, n_old_userloc_tweets, n_geotag_tweets, n_loc_tweets)

if __name__ == "__main__":
	Process(sys.argv[1], '../data/dataset_samples/')