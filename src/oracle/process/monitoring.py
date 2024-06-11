import typing as t

from web3 import Web3
from web3.contract.contract import Contract, ContractEvent

from src.oracle.models.oracle_requests import OracleRequest
from src.oracle.common.request_parameters import RequestType


class Monitoring:
    contract: t.Type[Contract]

    def __init__(self, w3_client: Web3, oracle: Contract):
        self.w3 = w3_client
        self.oracle = oracle

    def __call__(self, from_block: int, max_amount: int = 100) -> t.List[OracleRequest]:
        event_params = {
            event: self.grab_parameters(event)
            for event in self.grab_events(from_block, max_amount)
        }

        return self.setup_request_object(event_params)

    def grab_events(
        self, from_block: int, max_amount: int = 100
    ) -> t.List[ContractEvent]:
        event: ContractEvent = self.oracle.events.RequestCreated()
        events = event.get_logs(
            fromBlock=from_block,
        )

        return events[:max_amount]

    def grab_parameters(self, event: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        request_id = event["args"]["requestId"]
        block_number = event["blockNumber"]
        request_type = event["args"]["requestType"]

        event_name = RequestType(request_type).name
        param_event_cls: ContractEvent = getattr(self.oracle.events, event_name)
        param_events = param_event_cls.get_logs(
            fromBlock=block_number, toBlock=block_number
        )

        params = {}

        for param_event in param_events:
            if param_event["args"]["requestId"] == request_id:
                params = dict(param_event["args"])
                break

        assert params, "Error. Params could not be found"

        del params["requestId"]

        return params

    def setup_request_object(
        self, event_param_dict: t.Dict[ContractEvent, t.Dict[str, t.Any]]
    ) -> t.List[OracleRequest]:
        requests = []
        for event in event_param_dict:
            request = OracleRequest(
                requester=event["args"]["requester"],
                request_type=event["args"]["requestType"],
                request_timestamp=self.w3.eth.get_block(event["blockNumber"]).timestamp,
                callback_cost=0,
                charged_callback_gas=event["args"].get("chargedGas"),
                callback_timestamp=0,
                request_parameters=event_param_dict[event],
            )
            request.save()
            requests.append(request)

        return requests
