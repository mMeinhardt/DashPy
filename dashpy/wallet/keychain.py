import hmac
import hashlib
from pycoin.symbols.tdash import network
from dashpy.wallet.addressbook import AddressBook


class Keychain():
    def __init__(self, keys):
        if keys == None:
            self.keys = None
        else:
            self.keys = []
            for key in keys:
                self.keys.append(network.parse.bip32(key))

    def get_hwifs(self):
        hwifs = []
        for key in self.keys:
            hwifs.append(key.hwif(as_private=1))
        return hwifs

    def get_address_book(self):
        addresses = []
        for key in self.keys():
            addresses.append(key.address())
        address_book = AddressBook(addresses)
        return address_book

    def add_keys(self, new_keys):
        for new_key in new_keys:
            self.keys.append(new_key)