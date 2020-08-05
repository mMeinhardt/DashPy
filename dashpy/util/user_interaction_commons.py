import dashpy.util.commons as commons

init_help = "Initializes a new wallet in the default directory.\nThis will override any existing wallet in the directory, so make sure you have backed up your current wallet."
check_balance_help = "Checks the current balance of the wallet and prints its value in DASH"
check_trx_history_help = "Prints a history of transactions for this wallet, up to the specified depth"
send_trx_help = "Creates, signs and sends a new transaction."
export_wallet_help = f"Exports the current wallet-data to an unencrypted file in the specified directory. If no path is given, the data gets saved in the users home directory under: {commons.DEFAULT_EXPORT_PATH}"
restore_help = f"Asks the user for a mnemonic sentence, then restores the wallet corresponding to the given mnemonics. If no path for the wallet data is given, the data will be saved in the users home directory under: {commons.DEFAULT_RESTORE_PATH}"
receive_help = "Prints a Dash-address that can be used for receiving funds"
menu_help = "Starts the application in interactive mode, displaying a menu."
generate_new_help = "Generates new addresses for usage."

init_desc = init_help + "Will ask the user for a passwort that is used for encrypting the wallet."
check_balance_desc = check_balance_help
check_trx_history_desc = check_trx_history_help
send_trx_desc = send_trx_help +  ' If no arguments for address and amount is given, this command will ask the user interactively for both.'
export_wallet_desc = export_wallet_help
restore_desc = restore_help
receive_desc = receive_help + ' Will try to print out an unsused address. If no unused addresses are available, it will print one randomly'
menu_desc = menu_help
generate_new_desc = generate_new_help



currency_symbols = ["EUR", "USD", "BTC"]