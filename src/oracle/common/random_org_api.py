import typing as t
import os
from uuid import uuid4

from rdoclient import RandomOrgClient
from google.cloud.firestore_v1.client import CollectionReference, DocumentReference

from src.oracle.database.connection import get_db_client
from src.oracle.models.signed_random import SignedRandom


class RandomOrg:
    client: RandomOrgClient
    db_table: CollectionReference

    def __init__(self):
        self.client = RandomOrgClient(os.getenv("random_org_api_key"))
        self.db_table = get_db_client().collection("random_metadata")

    def get_random_int(self, min: int, max: int) -> t.Tuple[int, SignedRandom]:
        res = self.client.generate_signed_integers(1, min, max)
        signed_random = self.save(res)
        num = res["data"][0]

        return num, signed_random

    def get_random_int_array(
        self, quantity: int, min: int, max: int
    ) -> t.Tuple[t.List[int], SignedRandom]:
        res = self.client.generate_signed_integers(quantity, min, max)
        signed_random = self.save(res)
        nums = res["data"]

        return nums, signed_random

    def save(self, metadata: t.Dict[str, t.Any]) -> SignedRandom:
        signed_random = SignedRandom(**metadata)
        signed_random.save()
        return signed_random
