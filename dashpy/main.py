import dashpy.commands as commands
import argparse
import dashpy.util.user_interaction_commons as ui_commons
import sys

def main():
    parser = argparse.ArgumentParser(prog="DashPy")
    subparsers = parser.add_subparsers(title="Valid commands", help="For further help on a command, use '<command> -h'")

    parser_init = subparsers.add_parser("init", help=ui_commons.init_desc)
    parser_init.set_defaults(func=commands.commanddict['init'])

    parser_check_balance = subparsers.add_parser("balance", help=ui_commons.check_balance_help,
                                                 description=ui_commons.check_balance_desc)
    parser_check_balance.add_argument('-c', '--currency',
                                      type=str,
                                      choices=ui_commons.currency_symbols,
                                      help="print the corresponding value additionally in the specified currency")
    parser_check_balance.set_defaults(func=commands.commanddict['balance'])

    parser_check_trx = subparsers.add_parser("transaction-history", help=ui_commons.check_trx_history_help, description=ui_commons.check_trx_history_desc)
    parser_check_trx.add_argument('-d', '--depth',
                                  type=int,
                                  help='specifies how many past transaction are printed. Default is 10')
    parser_check_trx.set_defaults(func=commands.commanddict['transaction history'])

    parser_send_trx = subparsers.add_parser("send", help=ui_commons.send_trx_help, description=ui_commons.send_trx_desc)
    parser_send_trx.add_argument('-a', '--address',
                                 type=str,
                                 help='The address of the recipient. Must be a valid Dash-address')
    parser_send_trx.add_argument('-f', '--funds',
                                 type=float,
                                 help='The amount of funds to send in DASH.')
    parser_send_trx.set_defaults(func=commands.commanddict['send'])

    parser_export = subparsers.add_parser("export", help=ui_commons.export_wallet_help, description=ui_commons.export_wallet_desc)
    parser_export.add_argument('-p', '--path',
                               type=str,
                               help='The path to the file that is used for the export.')
    parser_export.set_defaults(func=commands.commanddict['export'])

    parser_restore = subparsers.add_parser("restore", help=ui_commons.restore_help, description=ui_commons.restore_desc)
    parser_restore.add_argument('-p', '--path',
                                type=str,
                                help='The path to the file in which the wallet data is restored.')
    parser_restore.set_defaults(func=commands.commanddict['restore'])

    parser_receive = subparsers.add_parser("receive",
                                           help=ui_commons.receive_help,
                                           description=ui_commons.receive_desc)
    parser_receive.set_defaults(func=commands.commanddict['receive'])

    parser_menu = subparsers.add_parser("menu", help=ui_commons.menu_help, description=ui_commons.menu_desc)
    parser_menu.set_defaults(func=commands.commanddict['menu'])


    parser_generate_new = subparsers.add_parser("generate-addresses",
                                                help=ui_commons.generate_new_help,
                                                description = ui_commons.generate_new_desc)
    parser_generate_new.add_argument('-n', '--number',
                                     type=int,
                                     help="The amount of new addresses to be generated.")
    parser_generate_new.set_defaults(func=commands.commanddict["generate-addresses"])

    parser_import = subparsers.add_parser("import",
                                          help=ui_commons.import_help,
                                          description=ui_commons.import_desc)
    parser_import.add_argument('-p', '--path',
                               type=str,
                               help="The path to the wallet file to be imported.")
    parser_import.set_defaults(func=commands.commanddict["import"])

    if(len(sys.argv) == 1):
        args = parser.parse_args(["--help"])
    else:
        args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()