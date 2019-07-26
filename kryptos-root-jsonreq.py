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


def send_exploit(exploit, sign):
    queryurl = BASEHOST + "/eval"
    logger.critical("Sending exploit...")
    payload = {
        "expr": "EXPLOIT HERE",
        "sig": "SIGNATURE HERE"
    }
    r = requests.post(queryurl, json=payload)
    try:
        logger.info(r.json())
    except:
        logger.error("Error: Payload Error!")
        logger.error(r.text)


def printusage():
    print("Usage: " + sys.argv[0] + " <Base64-encoded Payload> <Base64-encoded Signature>")


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
    for i in range(1, 101):
        rand = i
        sk = SigningKey.from_secret_exponent(rand, curve=NIST384p)
        vk = sk.get_verifying_key()
        success_not = verify(vk, oridt, orisig)
        if success_not:
            FLAG = 1
            logger.critical("Rand is: " + str(rand))
            break
    if FLAG == 0:
        print("You may reset the machine, rand is large than 100.")
        sys.exit(0)


# def main(exploit):
def main():
    printusage()
    check_server()
    orid = get_dbg_info()
    try_bf(orid)
    # send_exploit(exploit)


if __name__ == '__main__':
    # if not sys.argv[1]:
    #     logger.info("Payload Not Found.")
    #     sys.exit(1)
    # main(base64.b64decode(sys.argv[1].encode()))
    main()
