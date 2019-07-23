#!/usr/bin/env python3

# PyCrypto AES-512-CBC

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os


def encrypt(key, filename):
    # Per Block: 64KiB
    chunksize = 64*1024
    # Original Filename: im_msg.txt
    outputFile = "en" + filename
    # fill the first X bits with 0 to let the string length == 16
    filesize = str(os.path.getsize(filename)).zfill(16)
    # Generarte IV
    IV = Random.new().read(16)

    # AES-512-CBC
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            # Write the first 16 bytes as file original length
            outfile.write(filesize.encode('utf-8'))
            # write 17-32 bytes as IV
            outfile.write(IV)

            while True:
                # Each time read 64 bytes from the original file
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    # copy the original file and append zero to 16-bytes * n
                    chunk += b' ' * (16 - (len(chunk) % 16))
                
                # Write encrypted bytes
                outfile.write(encryptor.encrypt(chunk))


def getKey(password):
    # AES Encrypt password is SHA256-ed original password in hex form.
    # Original Password: sahay
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


