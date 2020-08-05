import hmac
import hashlib
from pycoin.symbols.tdash import network
from dashpy.wallet.address_book import Address_book


class Keychain():
    def __init__(self, keys):
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
        address_book = Address_book(addresses)
        return address_book