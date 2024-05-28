import toml
from web3 import Web3


class Config:
    def __init__(self, w3: Web3):
        self.w3 = w3

    def get_initial_config(self):
        initial_config = {"last_block": self.w3.eth.block_number}
