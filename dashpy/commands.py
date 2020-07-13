import dashpy.util.commons as commons

def initialize():
    print("Ich initialisiere")

def check_balance(currency):
    print("3 Dash (30 EUR)")

def check_trx_history(depth=10):
    for i in range(depth):
        print(f"Ich bin Transaktion {i}")

def send_transaction(recv_addr, amount):
    print(f"Sende {amount} an {recv_addr}")

def export_wallet(path=commons.DEFAULT_EXPORT_PATH):
    print(f"Exportiere Wallet nach: {path}")

def restore_wallet(path=commons.DEFAULT_RESTORE_PATH):
    print(f"Wiederherstelle nach: {path}")

def recieve():
    print("Schick Geld an diese Adresse: ykjsadlkjdf8u2kljösd")

def main_menu():
    print("Ich bin das Hauptmenu")