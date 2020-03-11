# Module for reading  english dictionary file from /usr/share/dict

import logging
import secrets

def read_dict():
    dictionary = []
    try:
        dictfile = open('/usr/share/dict/american-english', 'r')
        logging.info('Opened dictionary file')
        for word in dictfile:
            dictionary.append(word)
        return dictionary
    except OSError:
        print('Could not find the dictionary file under /usr/share/dict/american-english')
    finally:
        dictfile.close()

# This function returns a list with randomly choosen words
def get_random_words(number):
    dictionary = read_dict()
    words = []
    for i in range(0, number):
        words.append(secrets.choice(dictionary))
    return words


