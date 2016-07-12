"""
Zikafinder 1.01
Created by Diandra Kubo
Modified by Artur Pimentel
Summer 2016 - University of Notre Dame
Fixing the locations
"""
import geopy
import requests
import sys
import os
import json
import numpy as np

from pprint import pprint
from place import Place
from datetime import datetime

class JSONwrapper():
	"""JSONwrapper is a class to pass strings by reference"""
	def setJSON(self, json):
		self.json = json

###############################################################################
class LocationFinder():
	"""
	Class that, given the type of the tweet location--user profile or none--
	should be able to find the location of it
	"""
	def __init__(self):
		self.string_format = 'utf-8'
		self.gmaps_keys = self.get_googlemaps_keys()
		self.key_index = 0
		self.log_file = '../data/logs/location_finder_log.txt'
		
	def str_deformat(self, s):
		return s.decode(self.string_format)
		
	def str_format(self, s):
		return s.encode(self.string_format)
		
	def get_googlemaps_keys(self):
		with open('../apikeys/googlemaps_keys.txt') as keys_file:
			keys = keys_file.readlines()
			keys = [x.strip('\n') for x in keys]
			return keys

	def make_api_request(self, location, json_wrapper):
		# Get raw information about a city
		response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?key=%s&address=%s' %
								(self.gmaps_keys[self.key_index], location.replace(' ', '+')))
		json_wrapper.setJSON(response.json())
		resp_status = json_wrapper.json['status']

		while resp_status == u'OVER_QUERY_LIMIT' or resp_status == u'REQUEST_DENIED':
			self.key_index += 1
			#log_file.write('Changing key: ' + str(self.key_index) + '\n')

			if self.key_index > (len(self.gmaps_keys)-1):
				#log_file.write('Keys ended' + '\n')
				return None
			else:
				response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?key=%s&address=%s' %
								(self.gmaps_keys[self.key_index], location.replace(' ', '+')))
				json_wrapper.setJSON(response.json())
				resp_status = json_wrapper.json['status']

		city_found = False
		for place in json_wrapper.json['results'][0]['address_components']:
			place_type = place[u'types']
			if cmp(place_type, [u'locality', u'political']) == 0:
				location = place['short_name']
				city_found = True
				break
		if not city_found:
			return None

		latitude = json_wrapper.json['results'][0]['geometry']['location']['lat']
		longitude = json_wrapper.json['results'][0]['geometry']['location']['lng']

		return Place(location, latitude, longitude)

	def find_location_coordinates(self, location):
		resp_json_payload = JSONwrapper()
		try:
			return self.make_api_request(location, resp_json_payload)
		except Exception as e:
			with open(self.log_file, 'a') as log_file:
				resp_status = resp_json_payload.json['status']

				log_file.write(location + e.args[0] + '\n')
				log_file.write('STATUS: ' + resp_status + '\n')

				if e.args[0] != 'list index out of range' or resp_status != u'ZERO_RESULTS':
					log_file.write(str(resp_json_payload.json))
					return None