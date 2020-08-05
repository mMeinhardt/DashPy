import requests
import json




def get_funds_from_addresses(addresses):
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