import typing as t
from dataclasses import dataclass

from src.oracle.models.oracle_requests import OracleRequest
from src.oracle.common.random_org_api import RandomOrg
from src.oracle.common.characters_metadata import CharacterMetadata
from src.oracle.common.pinata_api import PinataApi


class MintCharacterData(t.TypedDict):
    requestId: str
    characterId: str
    attributes: t.Annotated[t.List[int], 10]
    ipfsId: str


class ProcessRandom:
    randomOrg = RandomOrg()

    @classmethod
    def get_random_data(self, request_type: str, request: OracleRequest):
        rand_func = getattr(self, f"process_{request_type}")

        return rand_func(request)

    @classmethod
    def process_SingleRandUint(self, request: OracleRequest) -> t.Dict[str, t.Any]:
        raise NotImplementedError

    @classmethod
    def process_RandUintArray(self, request: OracleRequest) -> t.Dict[str, t.Any]:
        raise NotImplementedError

    @classmethod
    def process_MintCharacter(self, request: OracleRequest) -> MintCharacterData:
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

        response = PinataApi().pin_json(
            "character_metadata" + str(request.request_parameters["characterId"]),
            ipfs_json,
        )

        return MintCharacterData(
            requestId=signed_random.request_id,
            characterId=request.request_parameters["characterId"],
            attributes=nums,
            ipfsId=response.json()["IpfsHash"],
        )
