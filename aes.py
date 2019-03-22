# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 23:09:55 2019

@author: Ahmet Melih Serter
"""

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher:

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest() # Key Size=32

    def encrypt(self, raw):
        raw = base64.b64encode(raw.encode("cp857"))
        raw = self._pad(raw.decode("cp857"))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode("cp857")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64decode(self._unpad(cipher.decrypt(enc[AES.block_size:]))).decode("cp857")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
