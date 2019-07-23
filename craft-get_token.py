#!/usr/bin/env python3

import requests
import json

proxyDict = {
              "http"  : "socks5://127.0.0.1:42778",
              "https" : "socks5://127.0.0.1:42778",
            }

get_apikey = requests.get('https://api.craft.htb/api/auth/login', auth=('dinesh', '4aUh0A8PbVJxgd'), verify=False, proxies=proxyDict)
json_response = json.loads(get_apikey.text)
token = json_response['token']

print(token)

apikeynm = "X-Craft-Api-Token"

custom_head = {apikeynm: token}



