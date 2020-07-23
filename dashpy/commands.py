import dashpy.util.commons as commons

def initialize():
    print("Ich initialisiere")

def check_balance(currency):
    print(f"3 Dash (30{currency})")

def check_trx_history(depth=10):
    for i in range(depth):
        print(f"Ich bin Transaktion {i}")

def send_transaction(recv_addr, amount):
    print(f"Sende {amount} an {recv_addr}")

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

commanddict = {'init': initialize,
               'balance': check_balance,
               'transaction history': check_trx_history,
               'send': send_transaction,
               'export': export_wallet,
               'restore': restore_wallet,
               'receive': recieve,
               'menu': main_menu}