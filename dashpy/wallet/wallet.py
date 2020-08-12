import json
import os
import dashpy.util.trx_util as trx_util
from pycoin.symbols.tdash import network
from pycoin.vm.ScriptTools import ScriptTools
import pycoin.coins.bitcoin.Spendable as Spendable
import pycoin.coins.tx_utils as tx_utils
import dashpy.wallet.keychain as keychain
from dashpy.wallet.addressbook import AddressBook
from dashpy.wallet.keychain import Keychain
from dashpy.util import util
from dashpy.util import commons
import dashpy.dapi.dapi_wrapper as dapi


class Wallet():
    def __init__(self, seed, addresses=None, keys=None):
        self.seed = seed
        self.address_book = AddressBook(addresses)
        self.keychain = Keychain(keys)



    def get_balance(self):
        balance = dapi.get_balance_from_addresses(self.address_book.addresses)
        return balance

    def generate_change_address(self):
        root_key = network.keys.bip32_seed(self.seed)
        n_current_keys = len(self.keychain.keys)
        new_key = root_key.subkey_for_path('0/0/0/' + str(n_current_keys))
        self.keychain.keys.append(new_key)
        self.address_book.addresses.append(new_key.address())
        return self.address_book.addresses[-1]




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
            self.generate_new_adresses(1)
            address = self.address_book.addresses[-1]
            return (False, address)
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
        index = 0
        for trx in trxs:
            if index >= n:
                break
            trx_dict = {"txin": [], "txout": []}
            for txin in trx.txs_in:
                address = txin.address(network.address)
                duffs = trx_util.get_duffs_from_trxin(txin)
                is_own_addr = False
                if address in self.address_book.addresses:
                    is_own_addr = True
                trx_dict["txin"].append({"duffs": duffs, "address": address, "own": is_own_addr})
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
            index = index + 1
            yield trx_dict


    def create_and_send_transaction(self, to, amount):
        amount_duffs = util.dash_to_duff(amount)

        utxos = self.get_needed_utxos(amount_duffs)

        spendables = []
        for utxo in utxos[1]:
            spendable_dict = {"coin_value": utxo[0]["satoshis"],
                              "script_hex": utxo[0]["script"],
                              "tx_hash_hex": utxo[0]["txid"],
                              "tx_out_index": utxo[0]["outputIndex"],
                              }
            spendables.append(Spendable.Spendable.from_dict(spendable_dict))

        change_address = self.generate_change_address()
        change_amount = utxos[0] -  (amount_duffs + commons.TRANSACTION_FEE)
        outputs = [(change_address, change_amount)]
        outputs.append((to, amount_duffs))
        keys_to_sign = []
        for output in utxos[1]:
            keys_to_sign.append(self.keychain.keys[output[1]].wif())

        trx = tx_utils.create_signed_tx(network, spendables, outputs, wifs=keys_to_sign, fee=commons.TRANSACTION_FEE)

        dapi.send_trx(trx.as_bin())








    def get_needed_utxos(self, amount_duffs):
        amount_in = 0
        utxos = []
        index = 0
        for address in self.address_book.addresses:
            answer = dapi.get_utxo_from_address(address)
            for utxo in answer["result"]["items"]:
                amount = utxo["satoshis"]
                utxos.append((utxo, index))
                amount_in = amount_in + amount
                if(amount_in + commons.TRANSACTION_FEE) > amount_duffs:
                    return amount_in, utxos
            index = index + 1


    def create_change_address(self):
        self.generate_new_adresses()


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

