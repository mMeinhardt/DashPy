import os
import json
import dashpy.util.crypto_util as crypto_util
import dashpy.util.util as util
import dashpy.util.commons as commons
from dashpy.wallet.wallet import Wallet
import io




class Storage():
    def __init__(self, path):
        if not os.path.isdir(path):
            raise NotADirectoryError("The specified Path must be a directory.")
        self.path = path

    def decrypt_and_load_full_wallet(self, password, salt):
        address_json = self.decrypt_and_load_addresses(password, salt)
        keys_json = self.decrypt_and_load_keys(password, salt)
        addresses = json.loads(address_json)
        keys = json.loads(keys_json)["keys"]
        seed = bytes.fromhex(json.loads(keys_json)["seed"])
        new_wallet = Wallet.create_full_wallet(addresses, seed, keys)
        return new_wallet

    def decrypt_and_load_addresses(self, password, salt):
        address_json = None
        with open(self.path + commons.ADDRESSES_FILE_NAME, 'rb') as addr_file:
            addr_enc_data = addr_file.read()
            address_json =  crypto_util.decrypt_AES(addr_enc_data, password, salt)
        return address_json

    def decrypt_and_load_keys(self, password, salt):
        keys_json = None
        with open(commons.WALLET_PATH + commons.KEYCHAIN_FILE_NAME, 'rb') as keys_file:
            keys_enc_data = keys_file.read()
            keys_json = crypto_util.decrypt_AES(keys_enc_data, password, salt)
        return keys_json

    def save_and_encrypt(self, wallet, password, salt):
        addr_json = json.dumps(wallet.address_book.addresses)
        with open(commons.WALLET_PATH + commons.ADDRESSES_FILE_NAME, 'wb') as addr_file:
            addr_file.write(crypto_util.encrypt_AES(util.to_bytes(addr_json), password, salt))

        if wallet.keychain == None:
            keys_dict = {"keys": wallet.keychain.get_hwifs(), "seed": bytes.hex(wallet.seed)}
            keys_seed_json = json.dumps(keys_dict)
            with open(commons.WALLET_PATH + commons.KEYCHAIN_FILE_NAME, 'wb') as keys_file:
                keys_file.write(crypto_util.encrypt_AES(util.to_bytes(keys_seed_json), password, salt))


    def export_wallet(self, path, wallet):
        keys_hwifs = wallet.keychain.get_hwifs()
        export_seed = bytes.hex(wallet.seed)
        wallet_dict = {"addresses": wallet.address_book.addresses,
                       "keys": keys_hwifs,
                       "seed": export_seed}



        wallet_json = json.dumps(wallet_dict, indent=4)
        with open(path, 'w') as exported_wallet:
            exported_wallet.write(wallet_json)



    def import_wallet(self, path_to_file, password, salt):
        wallet_json = json.load(open(path_to_file))

        addr_json = json.dumps(wallet_json["addresses"], indent=4)
        with open(commons.WALLET_PATH + commons.ADDRESSES_FILE_NAME, 'wb') as addr_file:
            addr_file.write(crypto_util.encrypt_AES(util.to_bytes(addr_json), password, salt))

        keys_and_seed_dict = {"keys": wallet_json["keys"],
                     "seed": wallet_json["seed"]}
        keys_json = json.dumps(keys_and_seed_dict, indent=4)
        with open(commons.WALLET_PATH + commons.KEYCHAIN_FILE_NAME, 'wb') as keys_file:
            keys_file.write(crypto_util.encrypt_AES(util.to_bytes(keys_json), password, salt))

    def load_watching_only_wallet(self, password, salt):
        addresses_json = self.decrypt_and_load_addresses(password, salt)
        addresses = json.loads(addresses_json)
        wallet = Wallet.create_watching_only_wallet(addresses=addresses)
        return wallet