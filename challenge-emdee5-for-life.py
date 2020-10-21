#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from hashlib import md5

baseURL = 'http://46.101.16.203:30064/'

req = requests.session()
loginp = req.get(baseURL)
soup = BeautifulSoup(loginp.text,features='lxml')
elem1 = soup.select('body > h3')[0].text.strip()
print(elem1)
md5data = md5(elem1.encode()).hexdigest()
print(md5data)
postflag = req.post(baseURL, data={"hash": md5data})
print(postflag.text)

