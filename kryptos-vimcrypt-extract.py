#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

# https://github.com/DidierStevens/DidierStevensSuite/blob/master/xor-kpa.py
# https://gist.github.com/amtal/d482a2f8913bc6e2c2e0
# https://github.com/vim/vim/blob/master/src/crypt.c
# http://nlitsme.github.io/posts/vim-encryption/
# https://dgl.cx/2014/10/vim-blowfish

knowntext = "rijndael / "  # recover from .old file
knowntext_digit = []
for i in knowntext:
    knowntext_digit.append(ord(i))

# Blowfish/CFB + SHA-256 custom key derivation

f1 = open("assets/kryptos-creds.txt", "rb").read()
f1magic = f1[:12]
f1salt = f1[12:20]
f1iv = f1[20:28]
f1ciphertext = f1[28:]

f2 = open("assets/kryptos-extracted-creds.txt", "wb").write(f1ciphertext)
