from hashlib import sha384
from os.path import expanduser
import logging
import json


def authenticate(password, hwtoken):
    homedir = expanduser('~')
    try:
        with open(homedir + '/.dashpy/authentication.json') as json_file:
            validation_data = json.load(json_file)
    except Exception:
        print("DashPy could not locate the authentication file. Make sure it is located under ~/.dashpy")
    password_hash = sha384()
    password_hash.update((password + validation_data["PWSalt"]).encode('utf-8'))
    hwtoken_hash = sha384()
    hwtoken_hash.update(hwtoken.encode('utf-8'))
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Testing Password with SHA348 Hash:\n" + password_hash.hexdigest() + "\nagainst saved password:\n" + validation_data["Password"])
    logging.info("Testing HWToken with SHA348 Hash:\n" + password_hash.hexdigest() + "\nagainst saved HWToken:\n" +
                 validation_data["HWToken"])
    if((password_hash.hexdigest() == validation_data["Password"]) and (hwtoken_hash.hexdigest() == validation_data["HWToken"])):
        logging.info("Authentication succesfull")
        return True
    logging.info("Mismatch detected. Authentication failed")
    return False

def main():
    authenticate("wasd", "wasdwasd")

if __name__ == '__main__':
    main()
