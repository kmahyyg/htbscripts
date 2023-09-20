#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import argparse
import keyring
import subprocess
import json
import shutil
import os

parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='op', type=str, choices=["save", "connect", "reset", "show"], default="connect", help="operation")
parser.add_argument("-d", dest='dst', type=str, required=False, help="pwnbox ip address")
parser.add_argument("-u", dest="user", type=str, required=False, help="pwnbox username")
parser.add_argument("-p", dest='passwd', type=str, required=False, help="pwnbox ssh password")
cmdargs = parser.parse_args()

def main():
    sshclient = shutil.which("ssh")
    if not sshclient:
        raise AssertionError("ssh client not found")
    sshpass = shutil.which("sshpass")
    if not sshpass:
        raise AssertionError("sshpass not found")
    pwnboxIPFile = os.path.expandvars('${HOME}/.config/pwnbox-ip.json')
    # store
    if cmdargs.op == "save":
        if cmdargs.user == "" or cmdargs.passwd == "" or cmdargs.dst == "":
            raise AssertionError("user, dest ip, password are required. port is always 22.")
        pwnboxIPstr = cmdargs.dst
        with open(pwnboxIPFile, "w") as fd:
            fd.write(json.dumps({"user": cmdargs.user, "dstip": pwnboxIPstr}))
        keyring.set_password(pwnboxIPstr, cmdargs.user, cmdargs.passwd)
        print("done!")
        return
    # Prestart check
    if not os.path.exists(pwnboxIPFile):
        raise AssertionError("pwnbox ip record cannot be found")
    pwnboxIPConf = open(pwnboxIPFile,"r").read()
    serviceData = json.loads(pwnboxIPConf)
    if cmdargs.op == "show":
        print(serviceData)
        print("Password: ", keyring.get_password(serviceData["dstip"], serviceData["user"]))
        return
    if cmdargs.op == "reset":
        keyring.delete_password(serviceData["dstip"], serviceData["user"])
        os.remove(pwnboxIPFile)
        print("reset done.")
        return
    if cmdargs.op == "connect":
        cred = keyring.get_password(serviceData["dstip"], serviceData["user"])
        if cred is None:
            raise AssertionError("no saved cred, save first.")
        cmdl = [sshpass, "-p", cred, "ssh", "-oStrictHostKeyChecking=no", serviceData["user"] + "@" + serviceData["dstip"]]
        print(" ".join(cmdl))
        return


if __name__ == "__main__":
    main()

# this application will help you quickly connect to pwnbox from your local machine, and save your password in your current pc's keychain
# to use: after op==save, try `eval $(ssh2pwnbox)`. When pwnbox terminated, do op==reset
# to debug: op==show
# tested on MacOS
