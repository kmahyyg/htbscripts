#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import random
import time
from urllib.parse import quote_plus as urlencode
import requests

debug = True

if debug:
    host = '127.0.0.1:8181'
else:
    host = '10.10.10.122'

endp = '/login.php'
finaluri = 'http://' + host + endp

postparam = {"inputUsername": None, "inputOTP": None}

# Assume the LDAP Query is: `(&(username=blahblah)(token=blahblah))`

usrname = ''
postparam["inputUsername"] = urlencode(usrname)
postparam["inputOTP"] = str(random.randint(10000000, 99999999))
sess = requests.session()
try:
    sess.get('http://' + host + '/')
    r = sess.post(finaluri, data=postparam)
    if 'cannot login' in r.text.lower():
        pass
    else:
        pass
except requests.exceptions.ConnectionError as ce:
    print("Get Banned! Wait 6 mins.")
    time.sleep(360)
