import os
import json
import dashpy.util.crypto_util as crypto_util
import dashpy.util.commons as commons
import dashpy.wallet.wallet as wallet
import io




class storage():
    def __init__(self, path):
        if not os.path.isdir(path):
            raise NotADirectoryError("The specified Path must be a directory.")
        self.path = path

    def decrypt_and_load_full_wallet(self, password, salt):
        address_json = self.decrypt_and_load_addresses(password, salt)
        keys_json = self.decrypt_and_load_keys(password, salt)
        addresses = json.loads(address_json)["addresses"]
        keys = json.loads(keys_json)["keys"]
        seed = json.loads(keys_json)["seed"]
        new_wallet = wallet.wallet.create_full_wallet(addresses, seed, keys)
        return new_wallet



    def decrypt_and_load_addresses(self, password, salt):
        address_json = None
        with open(commons.WALLET_PATH + commons.ADDRESSES_FILE_NAME, 'r') as addr_file:
            addr_enc_data = addr_file.read()
            address_json =  crypto_util.decode_AES(addr_enc_data, password, salt)
        return address_json

    def decrypt_and_load_keys(self, password, salt):
        keys_json = None
        with open(commons.WALLET_PATH + commons.KEYCHAIN_FILE_NAME, 'r') as keys_file:
            keys_enc_data = keys_file
            keys_json = crypto_util.decode_AES(keys_enc_data, password, salt)
        return keys_json