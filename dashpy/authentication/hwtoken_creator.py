# Module for static random password creation for HWToken
import dashpy.util.dictionary_reader as dict
import dashpy.util.commons as commons
import secrets
import logging

def create_hwtoken():
    random_words = dict.get_random_words(commons.AMOUNTWORDS)
    random_bytes = []
    for i in range(0, commons.AMOUNTWORDS):
        random_bytes.append(secrets.token_bytes(commons.SIZEOFFILLBYTES))
    hwtoken = ''
    for i in range(0, len(random_words)):
        index = secrets.randbelow(len(random_words))
        hwtoken = hwtoken + random_words[index]
        del random_words[index]
        index = secrets.randbelow(len(random_bytes))
        hwtoken = hwtoken + random_bytes[index].hex()
        del random_bytes[index]
    hwtoken = hwtoken.replace('\n', '').replace('\r', '')
    return hwtoken