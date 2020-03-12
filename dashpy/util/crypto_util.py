# module containing different crypto modules such instant-digest of cryptographic hash functions

import hashlib as hash
import secrets
import dashpy.util.commons as commons

def get_sha384_hex(input):
    hasher = hash.sha384()
    hasher.update(input.encode('utf-8'))
    return hasher.hexdigest()

def get_sha256_hex(input):
    hasher = hash.sha3_256()
    hasher.update(input.encode('utf-8'))
    return hasher.hexdigest()

def create_salt():
    return secrets.token_hex(commons.SALTLENGTH)