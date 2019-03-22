# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 21:15:27 2019

@author: Ahmet Melih Serter
"""

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import Blowfish

class BlowfishCipher:

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest() # Key Size=32

    def encrypt(self, raw):
        raw = base64.b64encode(raw.encode("cp857"))
        raw = self._pad(raw.decode("cp857"))
        iv = Random.new().read(Blowfish.block_size)
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode("cp857")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:Blowfish.block_size]
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
        return base64.b64decode(self._unpad(cipher.decrypt(enc[Blowfish.block_size:]))).decode("cp857")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]