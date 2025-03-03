import typing as t
from uuid import uuid4
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from abc import ABC
import inspect

from firebase_admin import firestore


from oracle.database.connection import get_db_client


@dataclass
class BaseModel(ABC):
    id: str = field(init=False, default_factory=lambda: str(uuid4().hex))

    _created_at: datetime = field(init=False, default=firestore.SERVER_TIMESTAMP)

    _updated_at: datetime = field(init=False, default=firestore.SERVER_TIMESTAMP)

    def save(self) -> t.Self:
        self._updated_at = firestore.SERVER_TIMESTAMP
        entity_dict = self.as_dict(exclude_fields=["id"])
        client = get_db_client()

        db_ref = client.collection(self.__tablename__).document(self.id)
        db_ref.set(entity_dict)

        for key in (entity_dict := db_ref.get().to_dict()):
            setattr(self, key, entity_dict[key])

        return self

    @classmethod
    def get(cls, id: str):
        client = get_db_client()

        db_table = client.collection(cls.__tablename__)
        entity = db_table.document(id).get()
        if entity:
            return cls.from_dict({**entity.to_dict(), "id": entity.id})
        return None

    @classmethod
    def query_one(cls, *filters: firestore.FieldFilter):
        res = cls._query(*filters)
        res_dict = {**res[0].to_dict(), "id": res[0].id}
        if res:
            return cls.from_dict(res_dict)
        return None

    @classmethod
    def query_many(cls, *filters: firestore.FieldFilter):
        res = cls._query(*filters)
        return [cls.from_dict({**i.to_dict(), "id": i.id}) for i in res]

    @classmethod
    def _query(cls, *filters: firestore.FieldFilter):
        client = get_db_client()
        table = client.collection(cls.__tablename__)

        entities = table
        for filter in filters:
            entities = entities.where(filter=filter)
        return entities.get()

    @classmethod
    def from_dict(cls, data: t.Dict[str, t.Any]):
        required_params = {
            k: v for k, v in data.items() if k in inspect.signature(cls).parameters
        }

        entity = cls(**required_params)
        for key in data:
            if key not in required_params:
                setattr(entity, key, data[key])

        return entity

    def as_dict(self, exclude_fields: t.List = None):
        if not exclude_fields:
            exclude_fields = []

        entity_dict = asdict(self)

        for field in exclude_fields:
            del entity_dict[field]

        return entity_dict
