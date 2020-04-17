# module containing different crypto modules such instant-digest of cryptographic hash functions


import hashlib as hash
import secrets

def get_sha384_hex(input):
    hasher = hash.sha384()
    hasher.update(input.encode('utf-8'))
    return hasher.hexdigest()

def get_sha256_hex(input):
    hasher = hash.sha3_256()
    hasher.update(input.encode('utf-8'))
    return hasher.hexdigest()

def get_sha256_bytes(input):
    input = to_bytes(input)

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

def encode_data():


def create_salt():
    return secrets.token_hex(commons.SALTLENGTH)
