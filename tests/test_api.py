from dashpy.dapi import dapi_wrapper

def main():
    funds = dapi_wrapper.get_funds_from_addresses(["yNPbcFfabtNmmxKdGwhHomdYfVs6gikbPf"])
    print(type(funds))
    print(funds)




if __name__ == '__main__':
    main()
