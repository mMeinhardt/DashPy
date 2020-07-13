import dashpy.commands as commands
import argparse
import dashpy.util.user_interaction_commons as ui_commons

def main():
    parser = argparse.ArgumentParser(prog="DashPy")
    subparsers = parser.add_subparsers(title="Valid commands", help="For further help on a command, use '<command> -h'")
    parser_init = subparsers.add_parser("init", help=ui_commons.init_help)
    parser_check_balance = subparsers.add_parser("balance", help=ui_commons.check_balance_help)
    parser_check_trx = subparsers.add_parser("transaction history", help=ui_commons.check_trx_history_help)
    parser_send_trx = subparsers.add_parser("send", help=ui_commons.send_trx_help)
    parser_export = subparsers.add_parser("export", help=ui_commons.export_wallet_help)
    parser_restore = subparsers.add_parser("restore", help=ui_commons.restore_help)
    parser_receive = subparsers.add_parser("receive", help=ui_commons.receive_help)

    parser.parse_args(["--help"])


if __name__ == "__main__":
    main()