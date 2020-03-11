# Module for static random password creation for HWToken
import dashpy.util.dictionary_reader as dict
import dashpy.util.commons as commons
import secrets
import logging

def create_hwtoken():
    dictionary = dict.read_dict()
    random_words = []
    for i in range(0, commons.AMOUNTWORDS):
        random_words.append(secrets.choice(dictionary))
    logging.info('Generated ' + commons.AMOUNTWORDS + 'random words')
    random_bytes = []
    for i in range(0, commons.AMOUNTWORDS):
        random_bytes.append(secrets.token_bytes(commons.AMOUNTBYTES))
    hwtoken = ''
    for i in range(0, len(random_words))
        index = secrets.randbelow(len(random_words))
        hwtoken = random_words[index]
        del random_words[index]
    return hwtoken