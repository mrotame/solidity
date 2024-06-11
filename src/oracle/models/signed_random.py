import typing as t
from dataclasses import dataclass, field

from src.oracle.database.base_model import BaseModel


@dataclass
class SignedRandom(BaseModel):
    __tablename__ = "signed_random_metadata"

    data: t.List[t.Any]
    random: t.Dict[str, t.Any]
    signature: str

    request_id: int = field(default=0)
