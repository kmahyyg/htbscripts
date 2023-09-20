#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import argparse
import keyring
import subprocess
import json
import shutil
import os
import urllib.parse as uparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='op', type=str, choices=["save", "connect", "reset", "show"], default="connect", help="operation")
parser.add_argument("-d", dest='dst', type=str, required=False, help="pwnbox ip address")
parser.add_argument("-u", dest="user", type=str, required=False, help="pwnbox username")
parser.add_argument("-p", dest='passwd', type=str, required=False, help="pwnbox ssh password")
parser.add_argument("-s", dest='furl', type=str, required=False, help="full pwnbox url")
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
        if cmdargs.user == "" or (cmdargs.passwd == "" and cmdargs.dst == "") or cmdargs.furl == "":
            raise AssertionError("user, (dest ip, password)/(full url of viewer) are required. port is always 22.")
        pwnboxIPstr = ""
        pwnboxPwd = cmdargs.passwd
        if cmdargs.dst != "":
            pwnboxIPstr = cmdargs.dst
        if cmdargs.furl != "":
            u1 = uparse.urlparse(cmdargs.furl)
            if u1.netloc != "vnc.htb-cloud.com":
                raise AssertionError("Only HTB Viewer Full URL is supported.")
            u2 = dict(uparse.parse_qsl(u1.query))
            pwnboxPwd = u2["password"]
            r1 = u2["host"].index("bird/")
            pwnboxIPstr = u2["host"][r1 + len("bird/"):]
        if pwnboxPwd == "":
            raise SystemError("cannot parse url to retrive data")
        print("Host: ", pwnboxIPstr, " ,Password: ", pwnboxPwd)
        with open(pwnboxIPFile, "w") as fd:
            fd.write(json.dumps({"user": cmdargs.user, "dstip": pwnboxIPstr}))
        keyring.set_password(pwnboxIPstr, cmdargs.user, pwnboxPwd)
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