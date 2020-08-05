from dashpy.persistence.storage import Storage
from dashpy.wallet.wallet import Wallet


def main():
    storage = Storage("/home/meinhardt")
    wallet = storage.decrypt_and_load_full_wallet(b"asd", bytes.fromhex("bc8d6e8ec547bf53"))
    storage.export_wallet("/home/meinhardt/abc.json", wallet)





if __name__ == '__main__':
    main()
