import dashpy.util.crypto_util as crypto_util
import dashpy.util.util as util
import pyaes
import hashlib
import dashpy.mnemonics.mnemonics as mem













if __name__ == '__main__':
    sentence = mem.generate_mnemonic(b"This is my seeddddd!")
    for word in sentence:
        print(word)
    print(len(sentence))