import requests
import os,sys
from bs4 import BeautifulSoup

def get_vax_json(output_filename, date_formatted, district_id_str):
    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id_str}&date={new_format}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    source = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'html.parser')
    f = open(output_filename, "w")
    f.write(str(soup))
    f.close()