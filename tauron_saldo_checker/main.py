import time

import requests
from bs4 import BeautifulSoup
import json
from invoice import Invoice
from requests import adapters
import ssl
from urllib3 import poolmanager
import sys
import os

token = os.getenv("SUPERVISOR_TOKEN")

class TLSAdapter(adapters.HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLS,
                ssl_context=ctx)

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
s = requests.session()
s.mount('https://', TLSAdapter())

options = {}

def map_name_to_entity_name(name):
    name_entity_map = {
        'Prąd': 'tauron_prad',
        'Gaz': 'tauron_gaz'
    }
    return name_entity_map.get(name)


def send_entity_state(name, invoice):
    ha_headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    ha_payload = {
        "state": invoice.saldo,
        "attributes":{
            "date": invoice.date
        }
    }
    ha_response = requests.post("http://supervisor/core/api/states/sensor."+name, json=ha_payload, headers=ha_headers)
    
    print(ha_response.status_code)
    print(ha_response.text)


def load_options():
    global options
    f = open("/data/options.json", "r")
    options = json.loads(f.read())
    f.close()


def login_():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'username': options['username'],
        'password': options['password'],
        'service': ''
    }
    s.get('https://logowanie.tauron.pl/')
    login = s.post('https://logowanie.tauron.pl/login', data=payload, headers=headers)
    return 'https://moj.tauron.pl/'


def get_saldo(body):
    if (body == None):
        saldo_page = s.get('https://moj.tauron.pl')
        p = BeautifulSoup(saldo_page.text, 'html.parser')
    else:
        p = BeautifulSoup(body, 'html.parser')
    print(p.title.text)
    
    invoice_raws = p.find_all(attrs={'class': 'amount-column'})
    invoice_raws = invoice_raws[:2]
    invoices = []
    for i in invoice_raws:
        print('---')
        name = i.parent.find_next('span').text
        si = float(i.find_next(attrs={'class': 'amount'}).text.replace(' zł', '').replace(',', '.').replace('+ ', ''))
        si = 0 if si == 0 else si * -1
        saldo = f'{si:.2f}'
        try:
            date = i.find_next(attrs={'class': 'date'}).text.replace('Termin: ', '')
        except:
            date = None
        invoice = Invoice(name, saldo, date)
        invoices.append(invoice)

    print(invoices)
    return invoices


if __name__ == '__main__':
    load_options()
    if (len(sys.argv) > 1 and sys.argv[1] == 'debug'):
        print('DEBUG')
        f = open("moj.tauron.pl.html", "r")
        body = f.read()
        f.close()
        saldos = get_saldo(body)
        for sa in saldos:
            send_entity_state(map_name_to_entity_name(sa.name), sa)
        sys.exit()
    
    while True:
        saldo_url = login_()
        saldos = get_saldo(None)
        for sa in saldos:
            send_entity_state(map_name_to_entity_name(sa.name), sa)
        time.sleep(60*5)
