#!/usr/bin/python
import json
import requests
import os,sys
import tweepy as tp
import time
import datetime 
from datetime import date
from json_parser import get_info_from_json, compare_availability_to_prev
from twitter_keys import mumbai_keys
from vax_scraper import get_vax_json

SCRAPED_JSON_FILENAME = "/home/ec2-user/vaxbot/jsons/adittest.json"
MUMBAI_DISTRICT_ID = "395"
SIMPLIFIED_INFO_FILENAME = "/home/ec2-user/vaxbot/jsons/simplified_info.json"
POSTED_TWEET_LOGFILE = "/home/ec2-user/vaxbot/tweets/logs.txt"
GENERAL_LOGILE = "/home/ec2-user/vaxbot/logger.txt"

def runner():
	today = date.today()
	NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
	new_format = today.strftime('%d-%m-%y')
	new_format2 = NextDay_Date.strftime('%d-%m-%y')
	scraped_json_filename = SCRAPED_JSON_FILENAME
	get_vax_json(scraped_json_filename, new_format, MUMBAI_DISTRICT_ID)
	parsed_info = get_info_from_json(scraped_json_filename)
	updated_avail, updated_sessions = compare_availability_to_prev(parsed_info, SIMPLIFIED_INFO_FILENAME)
	if updated_avail > 0:
		#send tweet here

		tweet_file = open(POSTED_TWEET_LOGFILE, "a")
		tweet = f'({new_format}) Mumbai has at least {updated_avail} new slots available this week. Book one now at cowin.gov.in #vaccine #cowin #covid #mumbairains'
		tweet_file.write(tweet + "\n")
		consumer_key = mumbai_keys['consumer_key']
		consumer_secret = mumbai_keys['consumer_secret']
		access_token = mumbai_keys['access_token']
		access_secret = mumbai_keys['access_secret']
		# login to twitter account api
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_secret)
		api = tp.API(auth)
		api.update_status(tweet)
		tweet_file.close()

	# updated extracted info json
	simplified_info_json = open(SIMPLIFIED_INFO_FILENAME, "w")
	json.dump(parsed_info, simplified_info_json)
	simplified_info_json.close()

	#update logs
	general_logfile = open(GENERAL_LOGILE, "a")
	general_logfile.write(f"latest run had {updated_avail} new appointments \n")
	general_logfile.close()




if __name__ == '__main__':
    runner()


#* * * * * /usr/local/bin/python3 /Users/Adit/Desktop/GitHub3/vaxbot/app.py
