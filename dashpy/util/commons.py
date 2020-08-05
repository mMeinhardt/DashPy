from pathlib import Path
import os

WALLET_PATH = (str(Path.home())) + os.path.sep + ".dashpy" + os.path.sep


AMOUNTWORDS = 10
SIZEOFFILLBYTES = 10
# The length of the salt in bytes
SALTLENGTH = 10
PBKDF2_ITERATIONS_ENCRYPTION = 100000
PBKDF2_ITERATION_MNEMONIC = 2048

MASTERKEY_HEADERS = {
    'xprv': 0x0488ade4,
    'xpub': 0x0488b21e
}

DEFAULT_EXPORT_PATH = (str(Path.home())) + os.path.sep + "exportedwallet.json"
DEFAULT_RESTORE_PATH = (str(Path.home())) + os.path.sep + "restoredwallet.json"

KEYCHAIN_FILE_NAME = "keys.json"
ADDRESSES_FILE_NAME = "addresses.json"
AUTH_FILE_NAME = "auth.json"



