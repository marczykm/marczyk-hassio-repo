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
    ha_response = requests.post("http://supervisor/core/api/states/sensor.smpiast_saldo", json=ha_payload, headers=ha_headers)
    print(ha_response.status_code)
    print(ha_response.text)


def load_options():
    global options
    f = open("/data/options.json", "r")
    options = json.loads(f.read())
    f.close()


def login_():
    global saldo_url
    index = s.get('https://ebok.smpiast.com.pl/ords/f?p=100:102::::RP,102::')
    parsed_html = BeautifulSoup(index.text, 'html.parser')
    salt = parsed_html.find(id='pSalt')['value']
    pageSubmissionId = parsed_html.find(id='pPageSubmissionId')['value']
    instance = parsed_html.find(id='pInstance')['value']
    pageItemsProtected = parsed_html.find(id='pPageItemsProtected')['value']
    p_json = {
        "pageItems": {
            "itemsToSubmit": [
                {"n": "P102_IP", "v": "80.68.239.20"},
                {"n": "P102_POMOC", "v": ""},
                {"n": "P102_USERNAME", "v": options['username']},
                {"n": "P102_PASSWORD", "v": options['password']}
            ],
            "protected": pageItemsProtected,
            "rowVersion": "", "formRegionChecksums": []},
        "salt": salt
    }
    payload = {
        'p_flow_id': 100,
        'p_flow_step_id': 102,
        'p_instance': instance,
        'p_debug': '',
        'p_request': 'P102_ZALOGUJ',
        'p_reload_on_submit': 'S',
        'p_page_submission_id': pageSubmissionId,
        'p_json': json.dumps(p_json)
    }
    login = s.post('https://ebok.smpiast.com.pl/ords/wwv_flow.accept', data=payload)
    redirectUrl = login.json()['redirectURL']
    return redirectUrl.replace('110', '24')


def get_saldo():
    global saldo
    saldo_page = s.get('https://ebok.smpiast.com.pl/ords/' + saldo_url)
    p = BeautifulSoup(saldo_page.text, 'html.parser')
    username = p.find_all(attrs={'class': 't-Button-label'})[0].text
    saldo = float(p.find_all(attrs={'class': 't-Card-desc'})[0].text.split(': ')[1].split(' (')[0].split(' zł')[0]
                  .replace(' ', '').replace(',', '.'))
    print(username)
    print(saldo)
    return saldo


if __name__ == '__main__':
    load_options()
    while True:
        saldo_url = login_()
        saldo = get_saldo()
        send_entity_state(saldo)
        time.sleep(60*5)

