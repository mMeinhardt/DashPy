import json
import os





class wallet():
    def __init__(self):
        pass


    def save_to_files(self, path):
        if not os.path.isdir(path):
            raise NotADirectoryError("The specified Path must be a directory.")


    @classmethod
    def create_full_wallet(cls, addresses, seed, keys):
        pass
