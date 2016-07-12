import googlemaps
from datetime import datetime
from pprint import pprint

gmaps = googlemaps.Client(key='AIzaSyBGgkR72eR10uEvzkWd0NaVIbArwOkDXG4')

# Geocoding an address
geocode_result = gmaps.geocode('Rua Dr. Alfredo Weyne, 55')
pprint(geocode_result)

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']))

for place in reverse_geocode_result:
	place_type = place['address_components'][0]['types']
	if cmp(place_type, [u'locality', u'political']) == 0:
		print place['address_components'][0]['short_name']