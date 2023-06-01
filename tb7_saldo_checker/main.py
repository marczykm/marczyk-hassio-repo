import time

import requests
from bs4 import BeautifulSoup
import json
import os

s = requests.Session()
options = {}

token = os.getenv("SUPERVISOR_TOKEN")
print("token: {}".format(token))

def send_entity_state(saldo):
    ha_headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    ha_payload = {
        "state": saldo
    }
    ha_response = requests.post("http://supervisor/core/api/states/sensor.tb7_saldo", json=ha_payload, headers=ha_headers)
    print(ha_response.status_code)
    print(ha_response.text)


def load_options():
    global options
    # f = open("/data/options.json", "r")
    f = open("options.json", "r")
    options = json.loads(f.read())
    f.close()


def login():
    global saldo_url
    payload = {
        'login': options['username'],
        'password': options['password']
    }
    login = s.post('https://tb7.pl/login', data=payload)
    print(login.url)

def get_saldo():
    global saldo
    saldo_page = s.get('https://tb7.pl/mojekonto')
    print(saldo_page.url)
    p = BeautifulSoup(saldo_page.text, 'html.parser')
    saldo = p.find_all(attrs={'class': 'textPremium'})[0].text.split(':')[-1].strip()
    print(saldo)
    return saldo


if __name__ == '__main__':
    load_options()
    while True:
        login()
        saldo = get_saldo()
        send_entity_state(saldo)
        time.sleep(60*30)

