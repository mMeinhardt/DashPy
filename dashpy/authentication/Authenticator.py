from hashlib import sha384
from os.path import expanduser
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
    del password
    hwtoken_hash = sha384()
    hwtoken_hash.update(hwtoken.encode('utf-8'))
    del hwtoken
    if((password_hash.hexdigest() == validation_data["Password"]) and (hwtoken_hash.hexdigest() == validation_data["HWToken"])):
        return True
    return False

