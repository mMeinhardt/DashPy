from hashlib import sha384
from os.path import expanduser
import dashpy.util.crypto_util as crypto
import dashpy.util.util as util
import dashpy.util.commons as commons
import logging
import json
import secrets
import hashlib

def save_pw(password):
    salt = secrets.token_hex(8)
    pwhash = hashlib.pbkdf2_hmac('sha384', util.to_bytes(password), bytes.fromhex(salt), 100000)
    pw_dict = {"password": pwhash.hex(), "salt": salt}
    json_str = json.dumps(pw_dict, indent=4)
    with open(commons.WALLET_PATH + commons.AUTH_FILE_NAME, "w") as auth_file:
        auth_file.write(json_str)


def get_salt():
    with open(commons.WALLET_PATH + commons.AUTH_FILE_NAME, 'r') as file:
        auth_json = json.load(file)
        return auth_json["salt"]

def get_saved_pw_hash():
    with open(commons.WALLET_PATH + commons.AUTH_FILE_NAME, 'r') as file:
        auth_json = json.load(file)
        return auth_json["password"]


def authenticate(password):
    salt = get_salt()
    pwhash = hashlib.pbkdf2_hmac('sha384', util.to_bytes(password), bytes.fromhex(salt), 10000)
    if pwhash.hex() == get_saved_pw_hash():
        return True
    return False
