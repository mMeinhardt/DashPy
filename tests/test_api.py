from dashpy.dapi import dapi_wrapper
from pycoin.symbols.tdash import network
from pycoin.cmds import tx

def main():
    addresses = ["yc2oeskpmewivXFKm4EG7pR4nWwe1LfaSY",
        "yZVMWRJWqwzzEV7ZEbcBdHNEXbgCtWjrq4",
        "ycr9Y83HqTZe95Wz5vEkHRHxHsCgQLWbwi",
        "yUQG7FxdJ8iSjLkUpGNdA1v1NW1agx3jTS",
        "yTdLuwP57zAHG226T6GRDJr9Mr61zWS5fS",
        "yduSocNoSR9UVseGkyP8eHUVMNSffyX5gN",
        "yReqATafmwpBDCPnTJ4cgBwEu2i5qLoDy4",
        "yj9Bvgw1C1mK6FxZeVPL8gwZaUuLRkbqHt",
        "ySGvCZKpG7XvkTt3YMeaoyfuASrS1XwaCT",
        "yjPriyL7aiJv3Dc4VoSbpzqcdgBqeZQY44",
        "yetoB1tWSHRT5BBGVYhEMwmpifG3YBBwyn",
        "yjKuMomHejfyo1fn94GCmYNdaKQ6fJnHRH",
        "yUA7NuYbeadn8wiRpxiWE1MHtFYda5MaW2",
        "yfaq5oDmqjjQ2QAhktwgT6hbzMo1uyDf34",
        "yMxpLM1BEpX3to7jGuicX3bzNVrXGLETs8",
        "yfM65KoQjNS1VjaevoF95j3u6yKFhFwh1V",
        "ygqXqpvVYDhJWnbvNTdrQMWZw3XkzDRMhQ",
        "yZKgVPbr2o6PfGbsy357ARhyPBazfU5MGL",
        "yUVyghePVc698DXtsc8e2zkdB6wPF5c24U",
        "yYJpVsJYjajsZhrfEuojKLhof5voeHrxDB",
        "yREDzY8Aprm3JLYm63qXk4uKs7gT275XRB",
        "yTdku1cyDbwaFAcVRgNwWRAyo27rFL6GXa"]
    transactions = dapi_wrapper.get_trxids_from_addresses(addresses)
    print(type(transactions))
    print(len(transactions))




if __name__ == '__main__':
    main()
