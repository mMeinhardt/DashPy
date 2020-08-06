import requests
import json

def main():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=DASH&vs_currencies=BTC"


    http_headers = {'content-type': 'application/json'}
    response_data_json = requests.request("GET", url, headers=http_headers)
    #response_data = json.loads(response_data_json.text)
    #print(response_data)
    print(response_data_json.text)




if __name__ == '__main__':
    main()