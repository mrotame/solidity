from unittest import TestCase
from random import randint

from oracle.process.process_random import ProcessRandom
from oracle.models.oracle_requests import OracleRequest


class TestProcessRandom(TestCase):

    def test_process_mint_character(self):
        mocked_request = OracleRequest(
            "10", 0, 0, 0, 0, 0, {"characterId": randint(1, 10000)}
        )
        mocked_request.id = randint(1, 10000)

        result = ProcessRandom.process_MintCharacter(mocked_request)

        self.assertEqual(result["requestId"], mocked_request.id)
        self.assertEqual(
            result["characterId"], mocked_request.request_parameters["characterId"]
        )

        self.assertEqual(len(result["attributes"]), 10)
