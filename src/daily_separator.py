import os
import json

from datetime import datetime
from dateutil import parser

direc = '../data/spring_dataset/'
files_list = os.listdir(direc)


start_date = parser.parse("Wed Mar 30 00:00:00 +0000 2016")

start_day = start_date	
end_day = parser.parse("Wed Mar 30 23:59:59 +0000 2016")
day_time = end_day - start_day
day = 31

day_f = open('../data/spring_data_daily/' + str(day) + '.json', 'w')
org_f = open('../data/spring_data_daily/orgfile.json', 'w')

with open('../data/spring_data_daily/orgfile3.json') as f:
	for line in f:
		if line != "\n":
			tweet = json.loads(line)
			tweet_time = parser.parse(tweet['created_at'])

			if tweet_time >= start_day and tweet_time <= end_day:
				day_f.write(line)
			elif tweet_time < start_day or tweet_time > end_day + day_time:
				org_f.write(line)
			else:
				day_f.close()
				day += 1
				day_f = open('../data/spring_data_daily/' + str(day).zfill(2) + '.json', 'w')

				start_day += day_time
				end_day += day_time