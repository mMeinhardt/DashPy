from hashlib import sha384
from os.path import expanduser
import json


def authenticate(passphrase, hwtoken):
    homedir = expanduser('~')
    try:
        with open(homedir + '/.dashpy/authentication.json') as json_file:
            validation_data = json.load(json_file)
    except Exception:
        print("DashPy could not locate the authentication file. Make sure it is located under ~/.dashpy")
    passphrase_hash = sha384()
    passphrase_hash.update((passphrase + validation_data["PWSalt"]).encode('utf-8'))
    hwtoken_hash = sha384()
    hwtoken_hash.update(hwtoken.encode('utf-8'))


def main():
    authenticate("123qweasd", "dasistderhashvomhwtoken")

if __name__ == '__main__':
    main()
