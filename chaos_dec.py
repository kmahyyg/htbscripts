#!/usr/bin/env python3
# Pycrypto AES-512-CBC 

from Crypto.Cipher import AES
import os
from Crypto.Hash import SHA256

def getKey(password):
    # AES Encrypt password is SHA256-ed original password in hex form.
    # Original Password: sahay
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def decrypt(key, filename):
    chunksize = 64 * 1024
    optFileName = "temp" + filename[2:]
    
    with open(filename, 'rb') as fie:
        with open(optFileName, 'wb') as fopt:
            originalFileSize = int(fie.read(16).decode('utf-8'))
            initialVector = fie.read(16)
            cipher = AES.new(key, AES.MODE_CBC, initialVector)
            while True:
                chunk = fie.read(chunksize)
                if len(chunk) == 0:
                    break
                fopt.write(cipher.decrypt(chunk))
     
    finalFileName = optFileName[4:]
    with open(optFileName, 'rb') as ftmp:
        tempf = ftmp.read(originalFileSize)
        with open(finalFileName, 'wb') as ffinal:
            ffinal.write(tempf)
    
    os.system('rm -f' + optFileName)
    
