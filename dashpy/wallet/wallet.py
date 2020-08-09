import json
import os
from pycoin.symbols.tdash import network
from pycoin.vm.ScriptTools import ScriptTools
import dashpy.wallet.keychain as keychain
from dashpy.wallet.addressbook import AddressBook
from dashpy.wallet.keychain import Keychain
from dashpy.util import util
import dashpy.dapi.dapi_wrapper as dapi


class Wallet():
    def __init__(self, seed, addresses=None, keys=None):
        self.seed = seed
        self.address_book = AddressBook(addresses)
        self.keychain = Keychain(keys)



    def get_balance(self):
        balance = dapi.get_balance_from_addresses(self.address_book.addresses)
        return balance

    def generate_new_adresses(self, n):
        root_key = network.keys.bip32_seed(self.seed)
        n_current_keys = len(self.keychain.keys)
        from_to_string = str(n_current_keys) + '-' + str(n_current_keys + (n-1))
        new_keys = root_key.subkeys('0/0/0/0/' + from_to_string)
        for key in new_keys:
            self.keychain.keys.append(key)
        for key in self.keychain.keys[n_current_keys:]:
            self.address_book.addresses.append(key.address())

    def get_recv_address(self):
        address = self.address_book.get_unused_address()
        if address is None:
            return (False, self.address_book.get_random_addr())
        return (True, address)


    def get_trx_history(self, n):
        trx_ids = dapi.get_trxids_from_addresses(self.address_book.addresses)
        trxs_bytes = []
        for trx_id in trx_ids:
            trxs_bytes.append(dapi.get_trx_details(trx_id))
        trxs = []
        for trx_bytes in trxs_bytes:
            trxs.append(network.Tx.from_hex(bytes.hex(trx_bytes)))
        parsed_trx = []
        print(len(trxs))
        for trx in trxs:
            trx_dict = {"txin": [], "txout": []}
            for txin in trx.txs_in:
                address = txin.address(network.address)
                is_own_addr = False
                if address in self.address_book.addresses:
                    is_own_addr = True
                trx_dict["txin"].append({"address": address, "own": is_own_addr})
            for txout in trx.txs_out:
                duffs = txout.coin_value
                api = network.address
                script_str = str(txout)
                scriptlist = script_str.split()
                script_pub = scriptlist[4][1:-1]
                address = api.for_p2pkh(bytes.fromhex(script_pub))
                is_own_addr = False
                if address in self.address_book.addresses:
                    is_own_addr = True

                out_dict = {"duffs": duffs, "address": address, "own": is_own_addr}
                trx_dict["txout"].append(out_dict)
            parsed_trx.append(trx_dict)

        n = n if n <= len(trxs) else len(trxs)
        print(len(parsed_trx))
        return parsed_trx



    @classmethod
    def create_full_wallet(cls, addresses, seed, keys):
        wallet = Wallet(seed, addresses=addresses, keys=keys)
        return wallet

    @classmethod
    def init_from_seed(cls, seed):
        root_key = network.keys.bip32_seed(seed)
        keys = root_key.subkeys('0/0/0/0/0-19')
        keys_hwifs = []
        addresses = []
        for key in keys:
            keys_hwifs.append(key.hwif(as_private=1))
            addresses.append(key.address())
        wallet = Wallet(seed, addresses=addresses, keys=keys_hwifs)
        return wallet

    @classmethod
    def create_watching_only_wallet(cls, addresses):
        wallet = Wallet(seed=None, addresses=addresses, keys=None)
        return wallet

