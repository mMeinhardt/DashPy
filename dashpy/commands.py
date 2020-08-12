import dashpy.util.commons as commons
import dashpy.util.util as util
import dashpy.authentication.authentication as authenticator
import getpass
from dashpy.wallet.mnemonics import generate_mnemonic_12words, mnemonic_to_seed, is_valid_mnemonic
from dashpy.wallet.wallet import Wallet
from dashpy.persistence.storage import Storage


def initialize(args):
    check_and_warn_if_wallet_exists()
    util.clear_console()
    print("Welcome to DashPy, a lightweight wallet application for the Dash Cryptocurrency.\n\n"
          "(Disclaimer: Please note that this Wallet is still WIP at an early stage, and not connected to the Dash Main-Net yet. Therefore it is not ready for productive usage.)\n\n"
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

def check_balance(args=None):
    check_if_wallet_init()
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()
    storage = Storage(commons.WALLET_PATH)
    wallet = storage.load_watching_only_wallet(util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    print("Your current Balance is:")
    print(f"{wallet.get_balance()} DASH")
    if args is not None:
        if args.currency:
            value = wallet.get_balance() * util.get_exchange_rate(args.currency)
            print(f"{round(value, 2)} {args.currency}") if args.currency in ["EUR", "USD"] else print(f"{value} {args.currency}")

def check_trx_history(args):
    check_if_wallet_init()
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()
    n = 10
    if args is not None and args.depth:
        n = args.depth
    storage = Storage(commons.WALLET_PATH)
    wallet = storage.decrypt_and_load_full_wallet(util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    i = 1
    for trx in wallet.get_trx_history(n):
        print(f"Transaction #{i}: ")
        print("From:")
        for txin in trx["txin"]:
            print(f"\t{util.duff_to_dash(txin['duffs'])}  Dash from {txin['address']}", end='')
            print(" (your address)") if txin["own"] else print("")
        print("To: ")
        for txout in trx["txout"]:
            print(f"\t{util.duff_to_dash(txout['duffs'])} DASH to {txout['address']}", end='')
            print(" (your address)") if txout["own"] else print("")
        print("")
        i = i+1


def send_transaction(args):
    check_if_wallet_init()
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()

    to = None
    funds = None

    if args is not None and args.address:
        to = args.address
    else:
        to = input("Enter the address you want to send DASH to: ")
    if args is not None and args.funds:
        funds = args.funds
    else:
        try:
            funds = float(input("Enter the amount to send in DASH: "))
        except ValueError:
            print("Not a valid number.\Exiting...")

    storage = Storage(commons.WALLET_PATH)
    wallet = storage.decrypt_and_load_full_wallet(util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    if wallet.get_balance() < (funds + util.duff_to_dash(commons.TRANSACTION_FEE)):
        print("Insufficient Funds for this transaction\nExiting...")
        exit(-1)
    if not util.is_dash_addr(to):
        print("Not a valid Dash-Address.\nExiting...")
        exit(-1)
    wallet.create_and_send_transaction(to, funds)
    print(f"Sent {funds} DASH to {to}")
    storage.save_and_encrypt(wallet, util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))








def export_wallet(args=None):
    check_if_wallet_init()
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()
    path = None
    if args is not None and args.path:
        path = args.path
    else:
        path = input("Enter the full path to the file in which you want the exported wallet files to be saved: ")
    try:
        storage = Storage(commons.WALLET_PATH)
        wallet = storage.decrypt_and_load_full_wallet(util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
        storage.export_wallet(path, wallet)
        print("Exported Wallet to: " + path)
    except Exception as e:
        print(e)
        print("Could not export the wallet to a file. Please check the specified path.")
        print("Exiting...")

def restore_wallet(args=None):
    check_if_wallet_init()
    path = None
    if args is not None and args.path:
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
    check_if_wallet_init()
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()
    storage = Storage(commons.WALLET_PATH)
    wallet = storage.load_watching_only_wallet(util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    recieve_response = wallet.get_recv_address()
    if not recieve_response[0]:
        print("Warning. You have no unused addresses left. Generating a new Address..."
              "\nYou can generate new addresses manually with the generate-addresses command.")

    print("Use this address to recieve Dash: ")
    print(recieve_response[1])

def main_menu(args=None):
    check_if_wallet_init()
    util.clear_console()
    print("Welcome to your Dash wallet")
    print("\n\nYour Options:")
    print("<1> - Show current balance")
    print("<2> - Show transaction history")
    print("<3> - Send DASH")
    print("<4> - Recieve DASH")
    print("<5> - Generate new addresses")
    print("<6> - Export wallet data")
    print("<7> - Import wallet data")
    print("<8> - Restore wallet via mnemonic sentence")
    print("<9> - Exit the wallet")
    ans = 0
    while True:
        try:
            ans = int(input("To choose an option, type in the corresponding number and hit Enter: "))
            if ans > 0 and ans < 10:
                break
            print("Not a valid choice.")
        except ValueError:
            print("Not a valid choice.")
    command = commandlist[ans-1]
    util.clear_console()
    command(None)

def import_wallet(args=None):
    check_if_wallet_init()
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()
    check_and_warn_if_wallet_exists()
    path = None
    if args is not None:
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
    check_if_wallet_init()
    password = getpass.getpass("Please type in your password: ")
    if not authenticator.authenticate(password):
        print("Wrong password. Exiting...")
        exit()
    n_new_addresses = 0
    if args is not None and args.number:
        n_new_addresses = args.number
    else:
        n_new_addresses = int(input("Enter how many new addresses should be generated: "))
    storage = Storage(commons.WALLET_PATH)
    wallet = storage.decrypt_and_load_full_wallet(util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    print("Generating " + str(n_new_addresses) + " new addresses...")
    wallet.generate_new_adresses(n_new_addresses)
    storage.save_and_encrypt(wallet, util.to_bytes(password), bytes.fromhex(authenticator.get_salt()))
    print("Done.")

def check_and_warn_if_wallet_exists():
    if (util.is_wallet_existing()):
        print("There is already a directory and files for an existing Wallet. Do you want to override them?\n"
              "Please note, that this action will make you most likely lose all your current keys, adresses and the corresponding funds.\n"
              "It is advised, that you back up the current wallet files first with the export command.\n")
        answer = input("Do you still want to continue? [yes/no]")
        if answer != "yes":
            print("Exiting...")
            exit()

def check_if_wallet_init():
    if not util.is_wallet_existing():
        print("There seems to be no existing wallet. Please run the init command first to create one.")
        exit()

command_dict = {'init': initialize,
               'balance': check_balance,
               'transaction-history': check_trx_history,
               'send': send_transaction,
               'export': export_wallet,
               'restore': restore_wallet,
               'receive': recieve,
               'menu': main_menu,
               'import': import_wallet,
               'generate-addresses': generate_new_addresses
                }

commandlist = [
    check_balance,
    check_trx_history,
    send_transaction,
    recieve,
    generate_new_addresses,
    export_wallet,
    import_wallet,
    restore_wallet,
    exit
    ]