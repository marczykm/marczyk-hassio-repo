import time

import requests
import os

token = os.getenv("SUPERVISOR_TOKEN")
print("token: {}".format(token))

options = {}

def send_entity_state(name, days, next_disposal):
    ha_headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    ha_payload = {
        "state": days,
        "attributes": {
            "next_disposal": next_disposal
        }
    }
    ha_response = requests.post("http://supervisor/core/api/states/sensor.brzezina_garbage_collection_"+name.lower().replace(' ', '').replace('ł', 'l'), json=ha_payload, headers=ha_headers)
    print(ha_response.status_code)
    print(ha_response.text)

def get_saldo():
    api_headers = {
        'x-skycms-key': '5d0123032115904c9d4ff70522405e60',
        'x-skycms-type': 'iOS',
        'x-skycms-device': '04C977DF-F4BB-4541-AEF2-EB2F454CB4D2'
    }
    api_response = requests.get('https://api.skycms.com.pl/api/v1/rest/garbage/disposals/8', headers=api_headers)
    print(api_response.status_code)
    print(api_response.json()['success'])
    kinds = api_response.json()['data']['garbage_kinds']
    for k in kinds:
        id = k['id']
        name = k['name']
        next_disposal = k['disposals'][0]
        send_entity_state(name, next_disposal['days'], next_disposal['id'])


if __name__ == '__main__':
    while True:
        get_saldo()
        time.sleep(60*60*8)