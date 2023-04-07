import time

import requests
from bs4 import BeautifulSoup
import json
import os

token = os.getenv("SUPERVISOR_TOKEN")
print("token: {}".format(token))

s = requests.Session()
options = {}
salt = ''
instance = ''

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
    # f = open("data/options.json", "r")
    options = json.loads(f.read())
    f.close()


def login_():
    global saldo_url, salt, instance
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
    print(login.text)
    redirectUrl = login.json()['redirectURL']
    return redirectUrl.replace('110', '24')


def get_saldo():
    global saldo, salt, instance
    saldo_page = s.get('https://ebok.smpiast.com.pl/ords/' + saldo_url)
    # time.sleep(5)
    p = BeautifulSoup(saldo_page.text, 'html.parser')
    js = p.find_all('script')[12].get_text()
    i = js.find('R_SALDO_WEDLUG_MIEJSC_24') + 27
    plugin = js[i:i+132]
    plugin = plugin.replace('\\', "/")
    plugin = plugin.replace('u002F', "")
    print('plugin: ' + plugin)
    p_json = {
        "salt": salt
    }
    payload = {
        'p_flow_id': 100,
        'p_flow_step_id': 24,
        'p_instance': instance,
        'p_debug': '',
        'p_request': 'PLUGIN='+plugin,
        'p_widget_action': 'reset',
        'x01': 31951121851046320,
        'p_json': json.dumps(p_json)
    }
    index = s.post('https://ebok.smpiast.com.pl/ords/wwv_flow.ajax', data=payload)
    p = BeautifulSoup(index.text, 'html.parser')
    saldo_text = p.find_all(attrs={'class': 't-Card-desc'})[0].get_text()
    i = saldo_text.find(':')+2
    saldo_text = saldo_text[i:-1]
    i = saldo_text.find('zł')
    saldo_text = saldo_text[0:i]
    saldo_text = saldo_text.replace(',', '.')
    print(saldo_text)
    saldo = float(saldo_text)
    
    return saldo


if __name__ == '__main__':
    load_options()
    while True:
        saldo_url = login_()
        saldo = get_saldo()
        send_entity_state(saldo)
        time.sleep(60*60)

