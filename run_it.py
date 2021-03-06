import requests
import easyconf.loader
import logging
from faker import Faker
import json
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
logging.getLogger('faker').setLevel(logging.INFO)

f = Faker()
PING_CONFIG = easyconf.loader.load_config("ping.yaml")
TOKEN = PING_CONFIG.get("TOKEN")
URL = PING_CONFIG.get("URL")

# 1.- create account
headers = {"Authorization":f"Token {TOKEN}"}


# create account
data = { 'name': f.first_name(),
        'external_id': f.pyint(), 
        'options':
            json.dumps([{
                'provider': 'telegram',
                'options': {
                    'message': 'msg default',
                    'chat_id': "-296140181",
                    'token': os.environ.get("TOKEN"),
                }
            }])
        }
log.info(data)
resp = requests.post(f"{URL}api/accounts/",data=data, headers=headers)

log.info(f"create account {resp.content}")
resp.raise_for_status()
account_id = resp.json().get("id")
assert account_id, f"not account_id {account_id}"

# create hostname
data = {
    'hostname':'62.171.189.208'
}
resp = requests.post(f"{URL}api/accounts/{account_id}/hosts/", data=data, headers=headers)
resp.raise_for_status()
log.info(f"create hosts {resp.content}")
host_id = resp.json().get("id")

data = {
    'default': True,
    'options': json.dumps([{
        'provider': 'telegram',
        'options':{
            'message': 'mesage 1',
        }
    }])
}
resp = requests.post(f"{URL}api/accounts/{account_id}/hosts/{host_id}/alerts/", data=data, headers=headers)
resp.raise_for_status()
log.info(f"create alerts {resp.content}")

