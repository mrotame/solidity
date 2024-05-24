import typing as t
from dotenv import load_dotenv

loaded = load_dotenv()

import os

from web3 import Web3
from web3.exceptions import ExtraDataLengthError

from pytypes.contracts.game.ArcaneWood import ArcaneWood


def get_abi(token) -> t.List[t.Dict[str, t.Any]]:
    abi = []
    for key in token._abi:
        abi.append(token._abi[key])

    return abi


class App:
    w3: Web3
    node_url = os.getenv("node_url")

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))

        assert self.w3.is_connected()

        try:
            self.w3.eth.get_block("latest")
        except ExtraDataLengthError:
            from web3.middleware import geth_poa_middleware

            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def start(self):
        WETH_ADDRESS = "0x6Da117feAb05963843F9E10972EFAB1d75bC17Dc"

        contract = self.w3.eth.contract(
            address=WETH_ADDRESS, abi=list(ArcaneWood._abi.values())
        )
        contract.events.Transfer().get_logs(fromBlock=self.w3.eth.block_number)

        block = self.w3.eth.get_block(40563329)
        for tx_hash in block.transactions:
            tx = self.w3.eth.get_transaction(tx_hash)
            if tx["to"] == WETH_ADDRESS:
                pass


if __name__ == "__main__":
    App().start()
