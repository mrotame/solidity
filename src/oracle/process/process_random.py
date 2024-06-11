import typing as t
from dataclasses import dataclass

from src.oracle.models.oracle_requests import OracleRequest
from src.oracle.common.random_org_api import RandomOrg
from src.oracle.common.characters_metadata import CharacterMetadata
from src.oracle.common.pinata_api import PinataApi


@dataclass
class RandomData:
    callback_response: t.Dict[str, t.Any]
    ipfs_json: t.Dict[str, t.Any]
    ipfs_metadata: t.Dict[str, t.Any] = None
    ipfs_options: t.Dict[str, t.Any] = None


class ProcessRandom:
    randomOrg = RandomOrg()

    @classmethod
    def get_random_data(self, request_type: int, request: OracleRequest):
        rand_func = getattr(self, f"process_{request_type}")

        return rand_func(request)

    @classmethod
    def process_SingleRandUint(self, request: OracleRequest):
        pass

    @classmethod
    def process_RandUintArray(self, request: OracleRequest):
        pass

    @classmethod
    def process_MintCharacter(self, request: OracleRequest) -> t.Dict[str, t.Any]:
        nums, signed_random = self.randomOrg.get_random_int_array(10, 0, 100)

        signed_random.request_id = request.id
        signed_random.save()

        ipfs_json = {
            **CharacterMetadata.build_character_metadata(nums),
            "randomness": {
                "data": signed_random.data,
                "random": signed_random.random,
                "signature": signed_random.signature,
            },
        }

        PinataApi().pin_json()
