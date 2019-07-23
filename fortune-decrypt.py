#!/usr/bin/env python3

import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

padding_string = b'}'

def pad(key):
    """Add padding to the key."""

    global padding_string
    str_len = len(key)

    # Key must be maximum 32 bytes long, so take first 32 bytes
    if str_len > 32:
        return key[:32]

    # If key size id 16, 24 or 32 bytes then padding not require
    if str_len == 16 or str_len == 24 or str_len == 32:
        return key

    # Convert bytes to string (python3)
    if not hasattr(str, 'decode'):
        padding_string = padding_string.decode()

    # Add padding to make key 32 bytes long
    return key + ((32 - str_len % 32) * padding_string)

    
def decrypt(ciphertext, key):
    """
    Decrypt the AES encrypted string.
    Parameters:
        ciphertext -- Encrypted string with AES method.
        key        -- key to decrypt the encrypted string.
    """

    global padding_string

    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(pad(key), AES.MODE_CFB, iv)
    decrypted = cipher.decrypt(ciphertext[AES.block_size:])

    return decrypted
    

cept = "utUU0jkamCZDmqFLOrAuPjFxL0zp8zWzISe5MF0GY/l8Silrmu3caqrtjaVjLQlvFFEgESGz".encode()
key4aes = "$pbkdf2-sha512$25000$z9nbm1Oq9Z5TytkbQ8h5Dw$Vtx9YWQsgwdXpBnsa8BtO5kLOdQGflIZOQysAy7JdTVcRbv/6csQHAJCAIJT9rLFBawClFyMKnqKNL5t3Le9vg".encode()
print(decrypt(cept,key4aes).decode())
