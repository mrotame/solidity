import typing as t
from dataclasses import dataclass, field

from oracle.database.base_model import BaseModel
from oracle.common import request_parameters as rp


@dataclass
class OracleRequest(BaseModel):
    __tablename__ = "requests"

    requester: str
    request_type: int
    request_timestamp: int
    callback_cost: int
    charged_callback_gas: int
    callback_timestamp: int
    request_parameters: t.Dict[str, t.Any]
    request_status: t.Literal["initialized", "processing", "completed", "failed"] = (
        field(init=False, default="initialized")
    )
