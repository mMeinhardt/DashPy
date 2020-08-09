import dashpy.dapi.dapi_wrapper as dapi
import random

class AddressBook():
    def __init__(self, addresses):
        self.addresses = addresses

    def add_addresses(self, new_addresses):
        self.addresses.append(new_addresses)
        print(self.addresses)
        print(len(self.addresses))

    def get_unused_address(self):
        for addr in self.addresses:
            if not dapi.is_address_used(addr):
                return addr
        return None

    def get_random_addr(self):
        return random.choice(self.addresses)