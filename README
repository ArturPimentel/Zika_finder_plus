ZikaFinder+ v1.01

tweet_sampler.py
	Collects data from twitter. It uses the keywords specified in src/param/crawler_keywords.txt to filter the search (one keyword per line in the text file). It also uses the authentication keys in apikeys/twitter_keys.json to run the tweepy API
	Usage: python tweet_sampler.py [(INT) # of tweets to be collected]
process_tweets.py
	Does the initial swap to see which tweets have some location information, and later on process all tweets with location data
	Usage: python process_tweets.py output.json > output.csv
fixLocations.py
	Calls the Google Geocoding API for each location description found to get the latitude and longitude 
	Usage: python fixLocations.py 
plota_mapas.py
	Plots the maps for each combination of keywords
	Usage: python plota_mapas.py output.csv

The order is:
Run tweet_sampler to get your data on a json file stored in data/crawler. If using for the first time, create a folder apikeys/ at the root and save your keys in the format:

{
	"consumer_key": "",
	"consumer_secret": "",
	"access_token": "",
	"access_token_secret": ""
}

inside a file called twitter_keys.json

Then run for the first time process_tweets (see more details on code).
To get the latitudes and longitudes from locations, run fixLocations.
Then you will run process_tweets for the second time, which will produce a csv file.
You will then use the csv file to produce the maps running the plota_mapas.

The html folder contains all the files we used for the website.
