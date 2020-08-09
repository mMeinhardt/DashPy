import dashpy.util.commons as commons

init_help = "Initializes a new wallet in the default directory.\nThis will override any existing wallet in the directory, so make sure you have backed up your current wallet."
check_balance_help = "Checks the current balance of the wallet and prints its value in DASH."
check_trx_history_help = "Prints a history of transactions for this wallet, up to the specified depth (10 by default)."
send_trx_help = "Creates, signs and sends a new transaction."
export_wallet_help = f"Exports the current wallet-data to an unencrypted file in the specified directory."
restore_help = f"Asks the user for a mnemonic sentence, then restores the wallet corresponding to the given mnemonics. If no Filepath is given, it will ask the user interactively for one."
receive_help = "Prints a Dash address from the wallet that can be used for receiving funds."
menu_help = "Starts the application in interactive mode, displaying a menu."
generate_new_help = "Generates new addresses for usage."
import_help = "Imports the wallet file from the specified path. Will overwrite any existing wallet files, including private keys and addresses"
main_help = "Lightweight CLI-based Wallet for the Dash Cryptocurrency. Makes usage of the Dash-Platform DAPI.\nDisclaimer: Please note that this Wallet is still WIP at an early stage, and not connected to the Dash Main-Net yet. Therefore it is not ready for productive usage."
sub_help = "For further help on a command, use '<command> -h'"

init_desc = init_help + "Will ask the user for a passwort that is used for encrypting the wallet."
check_balance_desc = check_balance_help
check_trx_history_desc = check_trx_history_help
send_trx_desc = send_trx_help +  ' If no arguments for address and amount is given, this command will ask the user interactively for both.'
export_wallet_desc = export_wallet_help
restore_desc = restore_help
receive_desc = receive_help + ' Will try to print out an unsused address. If no unused addresses are available, it will print one randomly.'
menu_desc = menu_help
generate_new_desc = generate_new_help
import_desc = import_help



currency_symbols = ["EUR", "USD", "BTC"]