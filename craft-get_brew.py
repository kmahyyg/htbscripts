#!/usr/bin/env python3

import requests
import json

# 10.10.10.110 Craft HTB
# 127.0.0.1:443 Forwarded
# Dump brew

urlbase = "https://api.craft.htb/api/brew/?page={pnum}&bool=false&per_page=50"

for i in range(1, 48):
    r = requests.get(urlbase.format(pnum=str(i)), verify=False)
    result = r.json()
    rfdcontent = json.dumps(result)
    rfd = open(str(i)+".json", "w")
    rfd.write(rfdcontent)
    rfd.flush()
    rfd.close()


