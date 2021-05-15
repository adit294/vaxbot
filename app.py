#!/usr/bin/python
import json
import requests
import os,sys
import tweepy as tp
import time
from datetime import date
from json_parser import get_info_from_json, compare_availability_to_prev
from vax_scraper import get_vax_json

SCRAPED_JSON_FILENAME = "/Users/Adit/Desktop/GitHub3/vaxbot/jsons/adittest.json"
MUMBAI_DISTRICT_ID = "378"
SIMPLIFIED_INFO_FILENAME = "/Users/Adit/Desktop/GitHub3/vaxbot/jsons/simplified_info.json"
POSTED_TWEET_LOGFILE = "/Users/Adit/Desktop/GitHub3/vaxbot/tweets/logs.txt"
GENERAL_LOGILE = "/Users/Adit/Desktop/GitHub3/vaxbot/logger.txt"

def runner():
	today = date.today()
	new_format = today.strftime('%d-%m-%y')
	scraped_json_filename = SCRAPED_JSON_FILENAME
	get_vax_json(scraped_json_filename, new_format, MUMBAI_DISTRICT_ID)
	parsed_info = get_info_from_json(scraped_json_filename)
	updated_avail, updated_sessions = compare_availability_to_prev(parsed_info, SIMPLIFIED_INFO_FILENAME)
	if updated_avail > 0:
		#send tweet here

		tweet_file = open(POSTED_TWEET_LOGFILE, "a")
		tweet = f'({new_format}) Mumbai has at least {updated_avail} new appointments available. Book one now at cowin.gov.in'
		tweet_file.write(tweet + "\n")
		consumer_key = ''
		consumer_secret = ''
		access_token = ''
		access_secret = ''
		# login to twitter account api
		auth = tp.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_secret)
		api = tp.API(auth)
		f = open("/Users/Adit/Desktop/GitHub3/vaxbot/tweets/logs.txt","r")
		api.update_status(f.read())
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


#* * * * * /Users/Adit/anaconda3/bin/python /Users/Adit/Desktop/GitHub3/vaxbot/app.py