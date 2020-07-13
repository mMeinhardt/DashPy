import hmac
import hashlib
import ecdsa
from pycoin.symbols.dash import network




def from_seed(seed):
    I = hmac.digest(b"Bitcoin seed", seed, hashlib.sha512)
    masterkey = I[0:32]
    masterchaincode = I[32:]
    secret = ecdsa.util.string_to_number(masterkey)
    point = ecdsa.ecdsa.generator_secp256k1 * secret


def get_pubkey_from_prv_key(prv_key):
    secret = ecdsa.util.string_to_number(prv_key)
    point = ecdsa.ecdsa.generator_secp256k1 * secret
    x = point.x()
    y = point.y()
    #pubkey_bytes =  bytes.fromhex((('%02x' % (2+(y&1))) + ('%064x' % x)))
    pubkey_bytes = ecdsa.ecdsa.Public_key(point, generator=ecdsa.ecdsa.generator_secp256k1)
    return pubkey_bytes.hex()