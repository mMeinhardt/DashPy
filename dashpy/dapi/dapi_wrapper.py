import requests
import json
import grpc
import base64
import dashpy.util.util as util
from dashpy.dapi.grpc_clients import core_pb2_grpc, core_pb2
from pycoin.symbols.tdash import network

def get_trxids_from_addresses(addresses):
    connection_url = "http://seed.evonet.networks.dash.org:3000/"
    payload = {"method": "getAddressSummary",
               "id": 1,
               "jsonrpc": "2.0",
               "params": {
                   "address": addresses
                   }
               }
    payload_json = json.dumps(payload)
    http_headers = {"content-type": "application/json"}
    response_data_json = requests.request("POST", connection_url, data=payload_json, headers=http_headers)
    response_data = json.loads(response_data_json.text)
    tx_ids = []
    for tx_id in response_data["result"]["transactions"]:
        tx_ids.append(tx_id)
    return tx_ids



def get_balance_from_addresses(addresses):
    connection_url = "http://seed.evonet.networks.dash.org:3000/"
    payload = { "method": "getAddressSummary",
                "id": 1,
                "jsonrpc": "2.0",
                "params": {
                    "address": addresses
                   }
               }

    payload_json = json.dumps(payload)
    http_headers = {'content-type': 'application/json'}
    response_data_json = requests.request("POST", connection_url, data=payload_json, headers=http_headers)
    response_data = json.loads(response_data_json.text)
    return response_data["result"]["balance"]

def get_trx_details(trx_id):
    channel = grpc.insecure_channel('seed.evonet.networks.dash.org:3010')
    stub = core_pb2_grpc.CoreStub(channel)
    request_object = core_pb2.GetTransactionRequest()
    request_object.id = trx_id
    response = stub.getTransaction(request_object)
    dec_string = base64.b64encode(response.transaction)
    hex_tx = bytes.hex(response.transaction)
    tx = network.Tx.from_hex(hex_tx)
    return tx

def is_address_used(address):
    connection_url = "http://seed.evonet.networks.dash.org:3000/"
    payload = {"method": "getAddressSummary",
               "id": 1,
               "jsonrpc": "2.0",
               "params": {
                   "address": [address]
               }
               }
    payload_json = json.dumps(payload)
    http_headers = {"content-type": "application/json"}
    response_data_json = requests.request("POST", connection_url, data=payload_json, headers=http_headers)
    response_data = json.loads(response_data_json.text)
    return response_data["result"]["txApperances"] > 0


def get_utxo_from_address(address):
    pass

def send_trx(transaction):
    pass