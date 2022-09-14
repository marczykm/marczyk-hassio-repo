import time

import requests
from bs4 import BeautifulSoup
import json
import os

token = os.getenv("SUPERVISOR_TOKEN")
print("token: {}".format(token))

s = requests.Session()
options = {}

def send_entity_state(saldo):
    ha_headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    ha_payload = {
        "state": saldo
    }
    ha_response = requests.post("http://supervisor/core/api/states/sensor.moico_saldo", json=ha_payload, headers=ha_headers)
    print(ha_response.status_code)
    print(ha_response.text)


def load_options():
    global options
    f = open("/data/options.json", "r")
    options = json.loads(f.read())
    f.close()


def login_():
    global saldo_url
    payload = {
        'loginform[login]': options['username'],
        'loginform[pwd]': options['password'],
        'loginform[submit]': 'Zaloguj się'
    }
    login = s.post('https://moico.internetunion.pl/?', data=payload)
    print(login.status_code)
    return 'https://moico.internetunion.pl/?m=info'


def get_saldo():
    global saldo
    saldo_page = s.get('https://moico.internetunion.pl/?m=finances')
    p = BeautifulSoup(saldo_page.text, 'html.parser')
    saldo_str = p.find_all(attrs={'class': 'conBoxLoginForm'})[1].text.replace('\n', '').split(' ')[1].split('\t')[0]
    print(saldo_str)
    saldo = float(saldo_str)
    return saldo


if __name__ == '__main__':
    load_options()
    while True:
        saldo_url = login_()
        saldo = get_saldo()
        send_entity_state(saldo)
        time.sleep(60*5)

