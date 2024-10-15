import time

import requests
from bs4 import BeautifulSoup
import json
import os

token = os.getenv("SUPERVISOR_TOKEN")

s = requests.Session()

def send_entity_state(price):
    print("TOKEN: " + str(token))
    ha_headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    ha_payload = {
        "state": price
    }
    ha_response = requests.post("http://supervisor/core/api/states/sensor.lidl_vacuum_price", json=ha_payload, headers=ha_headers)
    print(ha_response.status_code)
    print(ha_response.text)

def get_price():
    global price
    price_page = s.get('https://www.lidl.pl/p/silvercrest-robot-odkurzajacy-ssr-al1-z-aplikacja-i-nawigacja-laserowa/p100359709')
    p = BeautifulSoup(price_page.text, 'html.parser')
    price_str = p.find_all(attrs={'class': 'm-price__price'})[0].text
    price_str = price_str.replace(',', '.')
    print(price_str)
    price = float(price_str)
    return price


if __name__ == '__main__':
    print("Addon started")
    while True:
        price = get_price()
        send_entity_state(price)
        time.sleep(60*5)

