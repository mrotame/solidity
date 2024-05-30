from dotenv import load_dotenv

loaded = load_dotenv()

import typing as t
import os
import time

from web3 import Web3
from web3.exceptions import ExtraDataLengthError
from web3.contract.contract import Contract
from loguru import logger

from pytypes.contracts.oracle.Oracle import Oracle

from src.oracle.common.utils import get_abi
from src.oracle.process.monitoring import Monitoring


def get_abi(token) -> t.List[t.Dict[str, t.Any]]:
    abi = []
    for key in token._abi:
        abi.append(token._abi[key])

    return abi


class App:
    w3: Web3
    node_url = os.getenv("node_url")
    oracle: Contract

    monitoring: Monitoring

    def __init__(self):
        logger.info("Loading application...")
        self.config()
        self.start()

    def config(self):
        logger.info("Configuring app...")
        self.w3 = Web3(Web3.HTTPProvider(self.node_url))
        assert self.w3.is_connected()

        try:
            self.w3.eth.get_block("latest")
        except ExtraDataLengthError:
            from web3.middleware import geth_poa_middleware

            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.oracle = self.w3.eth.contract(
            Web3.to_checksum_address(os.getenv("oracle_address")), abi=get_abi(Oracle)
        )

        self.monitoring = Monitoring(self.w3, self.oracle)

    def start(self):
        logger.info("Starting process...")
        while True:
            self.run_process()
            time.sleep(1)

    def run_process(self):
        events = self.get_events()
        self.process_events(events)

    def get_events(self):
        events = self.monitoring(0)

    def process_events(self):
        pass

    def register_status(self):
        pass


if __name__ == "__main__":
    App()
