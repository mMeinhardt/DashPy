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
    pwhash = hashlib.pbkdf2_hmac('sha384', util.to_bytes(password), bytes.fromhex(salt), 10000)
    pw_dict = {"password": pwhash.hex(), "salt": salt}
    json_str = json.dumps(pw_dict, indent=4)
    with open(commons.WALLET_PATH + commons.AUTH_FILE_NAME, "w") as auth_file:
        auth_file.write(json_str)


def get_salt():
    with open(commons.WALLET_PATH + commons.AUTH_FILE_NAME, 'r') as file:
        auth_json = json.load(file)
        return auth_json["salt"]




def authenticate(password, hwtoken):
    homedir = expanduser('~')
    try:
        with open(homedir + '/.dashpy/authentication.json') as json_file:
            validation_data = json.load(json_file)
    except Exception:
        print("DashPy could not locate the authentication file. Make sure it is located under ~/.dashpy")
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Testing Password with SHA348 Hash:\n" + crypto.get_sha384_hex(password + validation_data["PWSalt"])
               + "\nagainst saved password:\n" + validation_data["Password"])
    logging.info("Testing HWToken with SHA348 Hash:\n" + crypto.get_sha384_hex(hwtoken)  + "\nagainst saved HWToken:\n" +
                 validation_data["HWToken"])
    if((crypto.get_sha384_hex(password + validation_data["PWSalt"]) == validation_data["Password"] ) and
        (crypto.get_sha384_hex(hwtoken) == validation_data["HWToken"])):
        logging.info("Authentication successful")
        return True

    #if((password_hash.hexdigest() == validation_data["Password"]) and (hwtoken_hash.hexdigest() == validation_data["HWToken"])):
    #    logging.info("Authentication succesfull")
    #    return True

    logging.info("Mismatch detected. Authentication failed")
    return False
