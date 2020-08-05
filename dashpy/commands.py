import os
import dashpy.util.commons as commons
import dashpy.util.util as util
import dashpy.authentication.authenticator as authenticator
import getpass
from dashpy.mnemonics.mnemonics import generate_mnemonic_12words, mnemonic_to_seed, is_valid_mnemonic
from dashpy.wallet.wallet import Wallet
from dashpy.persistence.storage import Storage


def initialize(args):
    check_and_warn_if_wallet_exists()
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
    util.clear_console()
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
    path = None
    if args.path:
        path = args.path
    else:
        path = input("Enter the full path to where you want the restored wallet files to be saved: ")
    print("Before restoring, please note: It is possible, that this implementation of the BIP39 protocoll is incompatible with the implementation of other wallet applications.\n")
    mnemonic_sentence = input("Type in your 12 word mnemonic sentence: ")
    if not is_valid_mnemonic(mnemonic_sentence):
        print("No valid mnemonic sentence.\nExiting...")
        exit()
    print("Restoring data...")
    wallet = Wallet.init_from_seed(mnemonic_to_seed(mnemonic_sentence))
    storage = Storage(commons.WALLET_PATH)
    try:
        print("Exporting Wallet to: " + path)
        storage.export_wallet(path, wallet)
        print("Done.")
    except Exception as e:
        print("Could not export the restored wallet to a file. Please check the specified path.")
        print("Exiting...")
        exit()






def recieve(args=None):
    print("Schick Geld an diese Adresse: ykjsadlkjdf8u2kljösd")

def main_menu(args=None):
    print("Ich bin das Hauptmenu")

def import_wallet(args=None):
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()
    if (util.is_wallet_existing()):
        print("There is already a directory and files for an existing Wallet. Do you want to override them?\n"
              "Please note, that this will make you most likely lose all your current keys, adresses and the corresponding funds."
              "It is advised, that you back up the current wallet files first with the export command.")
        answer = input("Do you still want to continue? [yes/no]")
        if answer != "yes":
            print("exiting...")
            exit()
    path = None
    if args.path:
        path = args.path
    else:
        path = input("Enter the full path to the wallet file you want to import: ")
    try:
        storage = Storage(commons.WALLET_PATH)
        print("Importing wallet data...")
        storage.import_wallet(path, util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
        print("Done.")
    except Exception as e:
        print("Error. Could not find a valid wallet file at your given path.")
        print("exiting...")
        exit()


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
    print("Generating " + n_new_addresses + " new addresses...")
    wallet.generate_new_adresses(n_new_addresses)
    storage.save_and_encrypt(wallet, util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    print("Done.")



def check_and_warn_if_wallet_exists():
    if (util.is_wallet_existing()):
        print("There is already a directory and files for an existing Wallet. Do you want to override them?\n"
              "Please note, that this action will make you most likely lose all your current keys, adresses and the corresponding funds."
              "It is advised, that you back up the current wallet files first with the export command.\n")
        answer = input("Do you still want to continue? [yes/no]")
        if answer != "yes":
            print("exiting...")
            exit()


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