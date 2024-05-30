import typing as t
from dataclasses import dataclass, field

from src.oracle.database.base_model import BaseModel
from src.oracle.common import request_parameters as rp


@dataclass
class Request(BaseModel):
    __tablename__ = "requests"

    requester: str
    request_type: int
    request_timestamp: int
    callback_cost: int
    charged_callback_gas: int
    callback_timestamp: int
    request_parameters: t.Dict[str, t.Any]
    completed: bool = field(init=False, default=False)
