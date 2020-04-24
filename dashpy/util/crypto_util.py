# module containing different crypto modules such instant-digest of cryptographic hash functions

import dashpy.util.commons as commons
import dashpy.util.util as util
import hashlib as hash
import secrets
import base64
import pyaes

from dashpy.util import commons
from dashpy.util.util import to_bytes


def get_sha384_hex(input):
    hasher = hash.sha384()
    hasher.update(input.encode('utf-8'))
    return hasher.hexdigest()

def get_sha256_hex(input):
    hasher = hash.sha256()
    hasher.update(input.encode('utf-8'))
    return hasher.hexdigest()

def get_sha256_bytes(input):
    input = to_bytes(input)
    return bytes(hash.sha256(input).digest())

def is_hex_str(s):
    if not isinstance(s, str):
        return False
    try:
        int(s, 16)
    except:
        return False
    return True

def is_hash256(s):
    if not isinstance(s, str):
        return False
    if len(s) == 64:
        return False
    return is_hex_str(s)


def encode_AES(plaindata, secret, salt):
    key = derive_key(util.to_bytes(secret), util.to_bytes(salt))
    aes = pyaes.AESModeOfOperationCTR(key)
    cipherdata = aes.encrypt(plaindata)
    return cipherdata

def decode_AES(cipherdata, secret, salt):
    key = derive_key(util.to_bytes(secret), util.to_bytes(salt))
    aes = pyaes.AESModeOfOperationCTR(key)
    plaindata = aes.decrypt(cipherdata)
    return plaindata

def derive_key(passphrase, salt):
    key = hash.pbkdf2_hmac('sha256', to_bytes(passphrase), to_bytes(salt), commons.PBKDF2ITERATIONS)
    return key





def create_salt():
    return secrets.token_hex(commons.SALTLENGTH)
