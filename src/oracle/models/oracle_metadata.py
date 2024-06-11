import typing as t
from dataclasses import dataclass, field
from firebase_admin.firestore import firestore

from src.oracle.database.base_model import BaseModel
from src.oracle.database.connection import get_db_client


@dataclass
class OracleMetadata(BaseModel):
    __tablename__ = "OracleMetadata"

    last_block_monitored: int = 0
    last_request_monitored: int = 0

    @classmethod
    def get_last(cls):
        client = get_db_client()
        table = client.collection(cls.__tablename__)

        query = table.order_by("_created_at").limit_to_last(1)
        entity = query.get()[0]

        return cls.from_dict({**entity.to_dict(), "id": entity.id})
