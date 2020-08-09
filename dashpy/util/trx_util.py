
from pycoin.symbols.tdash import network
from dashpy.dapi.dapi_wrapper import get_trx_details




def get_duffs_from_trxin(trxin):
    trx_id = str(trxin.previous_hash).encode()

    trx_bytes = get_trx_details(trx_id)
    parsed_trx = network.Tx.from_hex(bytes.hex(trx_bytes))
    duffs = parsed_trx.txs_out[trxin.previous_index].coin_value
    return duffs