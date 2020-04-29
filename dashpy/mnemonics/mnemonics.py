import dashpy.util.crypto_util as cryptoutil
import binascii
import os






def generate_mnemonic(seed):
    if len(seed) not in [16, 20, 24, 28, 32]:
        raise ValueError(f"The length of the seed has to be one of the following [16, 20, 24, 28, 32], but it is {len(seed)}")
    wordlist = load_wordlist()
    hash = cryptoutil.get_sha256_hex(seed)
    binary = (
            bin(int(binascii.hexlify(seed), 16))[2:].zfill(len(seed) * 8)
            + bin(int(hash, 16))[2:].zfill(256)[: len(seed) * 8 // 32]
    )
    mnemonic_sentence = []
    for i in range(len(binary) // 11):
        wordindex = int(binary[i * 11 : (i+1) * 11], 2)
        mnemonic_sentence.append(wordlist[wordindex])
    return mnemonic_sentence




def load_wordlist():
    with open(get_directory() + "/english.txt", "r") as file:
        wordlist = [word.strip() for word in file.readlines()]
    return wordlist


def get_directory():
    return os.path.join(os.path.dirname(__file__), "wordlists")

