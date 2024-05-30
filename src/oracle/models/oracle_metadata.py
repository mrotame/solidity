import typing as t
from dataclasses import dataclass, field
from firebase_admin.firestore import firestore

from src.oracle.database.base_model import BaseModel


@dataclass
class Monitoring(BaseModel):
    __tablename__ = "Monitoring"

    last_block_monitored: int = 0
    last_request_monitored: int = 0
