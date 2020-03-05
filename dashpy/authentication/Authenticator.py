from hashlib import sha384
from os.path import expanduser
import json


def authenticate(passphrase, hwtoken):
    homedir = expanduser('~')
    try:
        with open(homedir + '/.dashpy/authentication.json') as json_file:
            validation_data = json.load(json_file)
            print(validation_data)
    except Exception:
        print("DashPy could not locate the authentication file. Make sure it is located under ~/.dashpy")


def main():
    authenticate("abc123", "ichbineinhwtoken")

if __name__ == '__main__':
    main()
