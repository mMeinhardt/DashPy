


class Address_book():
    def __init__(self, addresses):
        self.addresses = addresses

    def add_addresses(self, new_addresses):
        self.addresses.append(new_addresses)
        print(self.addresses)
        print(len(self.addresses))

    def get_unused_address(self):
        return None