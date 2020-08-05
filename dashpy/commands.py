
import dashpy.util.commons as commons
import dashpy.util.util as util
import dashpy.authentication.authenticator as authenticator
import getpass
from dashpy.mnemonics.mnemonics import generate_mnemonic_12words, mnemonic_to_seed
from dashpy.wallet.wallet import Wallet
from dashpy.persistence.storage import Storage


def initialize(args):
    util.clear_console()
    print("Welcome to DashPy, a lightweight wallet application for the Dash Cryptocurrency.\n\n"
          "(Please note that this Wallet is still WIP at an early stage, and not connected to the Dash Main-Net yet.)\n\n"
          "It seems like this is your first time starting this application, so we will have to initialize a few things first.\n"
          "First, you have to enter a password. This is used for authentification and securing your wallet data on disk.\n")

    password = getpass.getpass("Please type in your password: ")
    re_password = getpass.getpass("Please type in your password again to confirm: ")
    while not password == re_password:
        password = getpass.getpass("The two given passwords don't match. Please type in your password again: ")
        re_password = getpass.getpass("Please type your password again to confirm: ")
    authenticator.save_pw(password)
    util.clear_console()
    print("""This is your mnemonic-sentence:\n""")
    mnemonic_sentence = generate_mnemonic_12words()
    print(mnemonic_sentence)
    print("\nPlease write these words down. They can be used to restore your complete wallet in case of a loss.\n"
          "It is advised against storing it on the same device as this wallet.\n")
    confirmation = input("Have you written down your mnemonic-sentence? (if so, type 'yes'): ")
    if confirmation != "yes":
        print("exiting...")
        exit(-1)
    print("Generating keys and addresses now...")
    seed = mnemonic_to_seed(mnemonic_sentence)
    wallet = Wallet.init_from_seed(seed)
    print("Saving and encrypting data on disk...")
    storage = Storage(commons.WALLET_PATH)
    storage.save_and_encrypt(wallet, util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    print("Done. You can now start using the Wallet. For a list of available commands type in 'dashpy --help'")



def check_balance(currency):
    print(f"3 Dash (30{currency})")

def check_trx_history(depth=10):
    for i in range(depth):
        print(f"Ich bin Transaktion {i}")

def send_transaction(args):
    if args.address and args.funds:
        print(f"Sende {args.funds} an {args.address}")

def export_wallet(path=commons.DEFAULT_EXPORT_PATH):
    print(f"Exportiere Wallet nach: {path}")

def restore_wallet(args=None):
    if args.path:
        print(f"Wiederherstelle nach: {args.path}")
    else:
        print(f"Wiederherstelle nach: {commons.DEFAULT_RESTORE_PATH}")

def recieve(args=None):
    print("Schick Geld an diese Adresse: ykjsadlkjdf8u2kljösd")

def main_menu(args=None):
    print("Ich bin das Hauptmenu")

def import_wallet(args=None):
    print("Ich importiere Wallets")

def generate_new_addresses(args=None):
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()
    n_new_addresses = 0
    if args.number:
        n_new_addresses = args.number
    else:
        n_new_addresses = int(input("Enter how many new addresses should be generated: "))
    storage = Storage(commons.WALLET_PATH)
    wallet = storage.decrypt_and_load_full_wallet(util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    wallet.generate_new_adresses(n_new_addresses)
    storage.save_and_encrypt(wallet, util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))


commanddict = {'init': initialize,
               'balance': check_balance,
               'transaction history': check_trx_history,
               'send': send_transaction,
               'export': export_wallet,
               'restore': restore_wallet,
               'receive': recieve,
               'menu': main_menu,
               'import': import_wallet,
               'generate-addresses': generate_new_addresses}