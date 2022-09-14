import time

import requests
from bs4 import BeautifulSoup
import json
import os

s = requests.Session()

def send_entity_state(price):
    token = os.getenv["SUPERVISOR_TOKEN"]
    print(token)
    ha_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    ha_payload = {
        "state": price
    }
    ha_response = requests.post("http://supervisor/core/api/states/sensor.ikea_strandmon", json=ha_payload, headers=ha_headers)
    print(ha_response.status_code)
    print(ha_response.text)

def get_price():
    global price
    price_page = s.get('https://www.ikea.com/pl/pl/products/844/80359844-compact-fragment.html')
    p = BeautifulSoup(price_page.text, 'html.parser')
    price_str = p.find_all(attrs={'class': 'pip-price__integer'})[0].text
    print(price_str)
    price = float(price_str)
    return price


if __name__ == '__main__':
    print("Addon started")
    while True:
        price = get_price()
        send_entity_state(price)
        time.sleep(60*5)

