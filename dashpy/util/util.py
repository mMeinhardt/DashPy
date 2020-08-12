import logging
import os
import dashpy.util.commons as commons
import dashpy.util.user_interaction_commons as ui_commons
import requests
import json

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')


def assert_bytes(data):
    assert isinstance(data, bytes)

def to_bytes(data, encoding='utf-8'):
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode(encoding)
    else:
        raise TypeError('Neither string or byte object')

def bytes_to_utf8(bytes_data):
    return bytes_data.decode()


def write_encrypted_data_to_file(data, path):
    assert_bytes(data)
    try:
        file = open(path, mode='wb')
        file.write(data)
        file.close()
    except IOError:
        logging.error(f'Could not write to {path}. Please make sure, you have sufficient permission for writing to the file.')
    finally:
        if file is not None:
            file.close()

def is_wallet_existing():
    if(os.path.exists(commons.WALLET_PATH)):
        return True
    return False

def get_exchange_rate(symbol):
    if symbol not in ui_commons.currency_symbols:
        raise ValueError("Not a currency symbol")
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=DASH&vs_currencies={symbol}"
    http_headers = {'content-type': 'application/json'}
    response_data_json = requests.request("GET", url, headers=http_headers)
    response = json.loads(response_data_json.text)
    return response["dash"][symbol.lower()]


def is_dash_addr(addr):
    if not isinstance(addr, str):
        return False
    if not addr[0] == 'y':
        return False
    if not 25 <= len(addr) <= 34:
        return False
    return True


def duff_to_dash(duff):
    return duff / 100000000

def dash_to_duff(dash):
    return int(dash * 100000000)

def mdash_to_duff(mdash):
    return int(mdash * 100000)

def mdash_to_dash(mdash):
    return mdash / 1000

def duff_to_mdash(duff):
    return duff / 100000

def dash_to_mdash(dash):
    return int(dash * 1000)





















