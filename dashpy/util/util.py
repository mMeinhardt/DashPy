import logging
import os
import dashpy.util.commons as commons

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