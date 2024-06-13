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
from src.oracle.models.oracle_requests import OracleRequest
from src.oracle.common.request_parameters import RequestType
from src.oracle.models.oracle_metadata import OracleMetadata
from src.oracle.process.process_random import ProcessRandom


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
            block_to_monitor = self.get_block_to_monitor()
            events = self.get_events(block_to_monitor)
            self.process_events(events)
            time.sleep(1)

    def get_events(self, from_block: int) -> t.List[OracleRequest]:
        events = self.monitoring(from_block)
        return events

    def process_events(self, events: t.List[OracleRequest]):
        for event in events:
            data = self.get_random_data(event)
            self.fulfill_request(event, data)

    def get_random_data(self, event: OracleRequest):
        request_type = RequestType(event.request_type).name
        request_type = request_type.replace("Params", "")

        rand_data = ProcessRandom.get_random_data(request_type, event)

        return rand_data

    def fulfill_request(self, event: OracleRequest, data: t.Dict[str, t.Any]):
        request_type = RequestType(event.request_type).name
        fulfill_func = getattr(self.oracle.functions, "fulfill" + request_type)
        fulfill_func(data)

    def get_block_to_monitor(self) -> int:
        last = OracleMetadata.get_last()
        return last.last_block_monitored


if __name__ == "__main__":
    App()
