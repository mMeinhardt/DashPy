import dashpy.util.crypto_util as crypto_util
import dashpy.util.util as util
import pyaes
import hashlib













if __name__ == '__main__':

    passwort = 'MeinPW'
    hwtoken = 'meinhwtoken'
    salt = 'verygoodsalt'

    plaintext = 'Dies ist der Plaintext'
    print(plaintext)
    encodedtext = crypto_util.encode_AES(plaintext, passwort+hwtoken, salt)
    print(encodedtext)

    decodedtext = crypto_util.decode_AES(encodedtext, passwort+hwtoken, salt)
    print(decodedtext)
    print(decodedtext.decode('utf-8'))
