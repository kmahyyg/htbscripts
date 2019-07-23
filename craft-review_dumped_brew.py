#!/usr/bin/env python3

import json
import time 

for i in range(1, 48):
    si = str(i)
    f1 = open(si+".json", "r").read()
    r1 = json.loads(f1)
    resl = r1["items"]
    for i in resl:
        print(i)
        time.sleep(0.5)

