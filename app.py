#!/usr/bin/python
import json
import requests
import os,sys
import tweepy as tp
import time
import datetime 
from datetime import date
from json_parser import get_info_from_json, compare_availability_to_prev
from twitter_keys import all_city_keys
from vax_scraper import get_vax_json

CITIES =["BOM"]
CITY_NAMES = {"BOM": "Mumbai"}
DISTRICT_IDS = {"BOM": "395"}
SCRAPED_JSON_FILENAME = "/home/ec2-user/vaxbot/jsons/{}/raw_scraped.json"
SIMPLIFIED_INFO_FILENAME = "/home/ec2-user/vaxbot/jsons/{}/simplified_info.json"
POSTED_TWEET_LOGFILE = "/home/ec2-user/vaxbot/tweets/{}/logs.txt"
CITY_LOGFILE = "/home/ec2-user/vaxbot/logs/{}/logger.txt"
GENERAL_LOGFILE = "/home/ec2-user/vaxbot/logger.txt"

def runner():
	today = date.today()
	NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
	new_format = today.strftime('%d-%m-%y')
	new_format2 = NextDay_Date.strftime('%d-%m-%y')
	for city in CITIES:
		scraped_json_filename = SCRAPED_JSON_FILENAME.format(city)
		get_vax_json(scraped_json_filename, new_format, DISTRICT_IDS[city])
		parsed_info = get_info_from_json(scraped_json_filename)
		updated_avail, updated_sessions = compare_availability_to_prev(parsed_info, SIMPLIFIED_INFO_FILENAME.format(city))
		if updated_avail > 0:
			#send tweet here

			tweet_file = open(POSTED_TWEET_LOGFILE.format(city), "a")
			city_name = CITY_NAMES[city]
			tweet = f'({new_format}) {city_name} has at least {updated_avail} new slots available this week. Book one now at cowin.gov.in #vaccine #cowin #covid #mumbairains'
			tweet_file.write(tweet + "\n")
			city_keys = all_city_keys[city]
			consumer_key = city_keys['consumer_key']
			consumer_secret = city_keys['consumer_secret']
			access_token = city_keys['access_token']
			access_secret = city_keys['access_secret']
			# login to twitter account api
			auth = tp.OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_token, access_secret)
			api = tp.API(auth)
			api.update_status(tweet)
			tweet_file.close()

		# updated extracted info json
		simplified_info_json = open(SIMPLIFIED_INFO_FILENAME.format(city), "w")
		json.dump(parsed_info, simplified_info_json)
		simplified_info_json.close()

		#update logs
		city_logfile = open(CITY_LOGFILE.format(city), "a")
		city_logfile.write(f"latest run had {updated_avail} new appointments \n")
		city_logfile.close()




if __name__ == '__main__':
    runner()


#* * * * * /usr/local/bin/python3 /Users/Adit/Desktop/GitHub3/vaxbot/app.py
