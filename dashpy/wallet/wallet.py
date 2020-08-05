import json
import os
from pycoin.symbols.tdash import network
import dashpy.wallet.keychain as keychain
from dashpy.wallet.address_book import Address_book
from dashpy.wallet.keychain import Keychain
from dashpy.util import util


class Wallet():
    def __init__(self, seed, addresses=None, keys=None):
        self.seed = seed
        self.address_book = Address_book(addresses)
        self.keychain = Keychain(keys)



    def get_balance(self):
        return 343984

    def generate_new_adresses(self, n):
        root_key = network.keys.bip32_seed(util.to_bytes(self.seed))
        n_current_keys = len(self.keychain.keys)
        from_to_string = str(n_current_keys) + '-' + str(n)
        new_keys = root_key.subkeys('0/0/0/0/' + from_to_string)
        self.keychain.add_keys(new_keys)
        addresses = []
        for key in new_keys:
            addresses = key.address()
        self.address_book.add_addresses(addresses)

    @classmethod
    def create_full_wallet(cls, addresses, seed, keys):
        wallet = Wallet(seed, addresses=addresses, keys=keys)
        return wallet

    @classmethod
    def init_from_seed(cls, seed):
        root_key = network.keys.bip32_seed(seed)
        keys = root_key.subkeys('0/0/0/0/0-20')
        keys_hwifs = []
        addresses = []
        for key in keys:
            keys_hwifs.append(key.hwif(as_private=1))
            addresses.append(key.address())
        wallet = Wallet(seed, addresses=addresses, keys=keys_hwifs)
        return wallet