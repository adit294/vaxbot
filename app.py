#!/usr/bin/python
import requests
import os,sys
import tweepy as tp
import time
from datetime import date
from bs4 import BeautifulSoup
today = date.today()
new_format = today.strftime('%d-%m-%y')
f = open("/Users/Adit/Desktop/vax_bot/adittest.txt","w")

def helper():

    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=400004&date={new_format}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    source = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'html.parser')
    f.write(str(soup))
    f.close()

f.write('hi')
if __name__ == '__main__':
    helper()

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

# login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)


f = open("/Users/Adit/Desktop/vax_bot/adittest.txt","r")
api.update_status(f.read())