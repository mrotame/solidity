import typing as t
import os
from uuid import uuid4

from rdoclient import RandomOrgClient as _RandomOrgClient
from google.cloud.firestore_v1.client import CollectionReference, DocumentReference

from oracle.database.connection import get_db_client
from oracle.models.signed_random import SignedRandom


class RandomOrg:
    client: _RandomOrgClient
    db_table: CollectionReference

    def __init__(self):
        self.client = _RandomOrgClient(os.getenv("random_org_api_key"))
        self.db_table = get_db_client().collection("random_metadata")

    def get_random_int(self, min: int, max: int) -> t.Tuple[int, SignedRandom]:
        res = self.client.generate_signed_integers(1, min, max)
        signed_random = self.get_signed_random(res)
        num = res["data"][0]

        return num, signed_random

    def get_random_int_array(
        self, quantity: int, min: int, max: int
    ) -> t.Tuple[t.List[int], SignedRandom]:
        res = self.client.generate_signed_integers(quantity, min, max)
        signed_random = self.get_signed_random(res)
        nums = res["data"]

        return nums, signed_random

    def get_signed_random(self, res: t.Dict[str, t.Any]) -> SignedRandom:
        signed_random = SignedRandom(
            data=res["data"], random=res["random"], signature=res["signature"]
        )
        return signed_random
