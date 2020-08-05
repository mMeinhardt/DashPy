from dashpy.persistence.storage import Storage
from dashpy.wallet.wallet import Wallet


def main():
    wallet = Wallet.init_from_seed(b"mein lieblingsseed")
    storage = Storage("/home/meinhardt")
    storage.export_wallet("/home/meinhardt/abc.json", wallet)
    storage.import_wallet("/home/meinhardt/abc.json", b"pw", b"salt")
    wallet = storage.decrypt_and_load_full_wallet(b"pw", b"salt")
    print("lol")
    print(wallet.address_book.addresses)
    print(wallet.seed)
    print(wallet.keychain.get_hwifs())
    storage.save_and_encrypt(wallet, b"pw", b"salt")




if __name__ == '__main__':
    main()
