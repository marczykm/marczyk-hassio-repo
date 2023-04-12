import time

import requests
import json
import os

token = os.getenv("SUPERVISOR_TOKEN")
print("token: {}".format(token))

s = requests.Session()
options = {}

def send_entity_state(saldo, deadline):
    ha_headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    ha_payload = {
        "state": saldo,
        "attributes": {
            "date": deadline
        }
    }
    ha_response = requests.post("http://supervisor/core/api/states/sensor.pgnig_saldo", json=ha_payload, headers=ha_headers)
    print(ha_response.status_code)
    print(ha_response.text)


def load_options():
    global options
    f = open("/data/options.json", "r")
    #f = open("data/options.json", "r")
    options = json.loads(f.read())
    f.close()


def login_():
    global saldo_url, salt, instance
    # index = s.get('https://ebok.pgnig.pl/auth/login?api-version=3.0')
    # parsed_html = BeautifulSoup(index.text, 'html.parser')
    # salt = parsed_html.find(id='pSalt')['value']
    # pageSubmissionId = parsed_html.find(id='pPageSubmissionId')['value']
    # instance = parsed_html.find(id='pInstance')['value']
    # pageItemsProtected = parsed_html.find(id='pPageItemsProtected')['value']
    # p_json = {
    #     "pageItems": {
    #         "itemsToSubmit": [
    #             {"n": "P102_IP", "v": "80.68.239.20"},
    #             {"n": "P102_POMOC", "v": ""},
    #             {"n": "P102_USERNAME", "v": options['username']},
    #             {"n": "P102_PASSWORD", "v": options['password']}
    #         ],
    #         "protected": pageItemsProtected,
    #         "rowVersion": "", "formRegionChecksums": []},
    #     "salt": salt
    # }
    payload = {
        "identificator": options['username'],
        "accessPin": options['password'],
        "rememberLogin": True,
        "reCaptcha":"03AKH6MRHZCHbJG0BJNBpnU5m6li8PX2tWQBeWWpWmaJDkMtQDqm2xrMpFxZ-RYQllpQMOjNYfLozGmApEA_UzkUbpHYn3ND4aDR-VK8N_LaIlQeGUtCcu1XqjJZCIakp5hCtuQPuDIECwrUlIBQM0xitOtSvaXckKRl8Uiiod8RddIqLs7kOVdvTAZC_cn1DJH8CJ0qpHqjZ_Y5YB4k6fXvEiJ3x8ls-6EFPaSRfc4J4L6Isldd7BKM5Ta3jal3dyD3cYfdLJNYzECDP-KADw02h54vrEAPgRiUqnzzjsAgeu6NzOmwm4iNYVyMaadSW6-XmEy-K88MakDVUEM6Zesw_NfDYBa4piSsGU5U9xWBumRzNTZYMuXzqPkvmlK7wFqp6CBn-SfI5ZPCmcxdVT6pxyuWEVXQCHSMoyiC5PmTTh2LX8BGfoxh6DJQL9csWgt7ka877o6RTXvWxLaA1WPSG1L-cMdS-bOq4gc4AgCO6NiQGVQEAb6URHRDq1yKTKMsJGysfdJoh2GvpOpgb5BGmQJwic3wf1UQ",
        "DeviceId":"7eae044acf7027fe5c9d19074b9e741c",
        "DeviceName":"Chrome wersja: 112.0.0.0<br>",
        "DeviceType":"Web"
    }
    login = s.post('https://ebok.pgnig.pl/auth/login?api-version=3.0', data=payload)
    print(login.text)
    # redirectUrl = login.json()['redirectURL']
    return 'https://ebok.pgnig.pl/'


def get_saldo():
    saldo_page = s.get('https://ebok.pgnig.pl/crm/get-invoices-v2?pageNumber=1&pageSize=12&api-version=3.0')
    saldo = float(saldo_page.json()['InvoicesList'][0]['AmountToPay'])
    deadline = saldo_page.json()['InvoicesList'][0]['PayingDeadlineDate']
    
    return saldo, deadline


if __name__ == '__main__':
    load_options()
    while True:
        saldo_url = login_()
        saldo, deadline = get_saldo()
        print(saldo)
        send_entity_state(saldo, deadline)
        time.sleep(60*60)