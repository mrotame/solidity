import typing as t
from dotenv import load_dotenv

loaded = load_dotenv()

import os

from web3 import Web3
from web3.exceptions import ExtraDataLengthError

from pytypes.contracts.game.ArcaneWood import ArcaneWood

from pytypes.contracts.oracle.Oracle import Oracle


def get_abi(token) -> t.List[t.Dict[str, t.Any]]:
    abi = []
    for key in token._abi:
        abi.append(token._abi[key])

    return abi


class App:
    w3: Web3
    node_url = os.getenv("node_url")
    oracle = Oracle(os.getenv("oracle_address"))

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))

        assert self.w3.is_connected()

        try:
            self.w3.eth.get_block("latest")
        except ExtraDataLengthError:
            from web3.middleware import geth_poa_middleware

            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def start(self):
        contract = self.w3.eth.contract(
            address=WETH_ADDRESS, abi=list(ArcaneWood._abi.values())
        )
        contract.events.Transfer().get_logs(fromBlock=self.w3.eth.block_number)

        block = self.w3.eth.get_block(40563329)
        for tx_hash in block.transactions:
            tx = self.w3.eth.get_transaction(tx_hash)
            if tx["to"] == WETH_ADDRESS:
                pass

    def run_process(self):
        events = self.slice_events(self.get_events())
        last_block = self.get_last_block(events[-1])

        self.process_events(events)

    def get_events(self):
        pass

    def slice_events(self):
        pass

    def get_last_block(self):
        pass

    def process_events(self):
        pass

    def register_status(self):
        pass


if __name__ == "__main__":
    App().start()
