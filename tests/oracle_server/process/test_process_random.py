from unittest import TestCase

from src.oracle.process.process_random import ProcessRandom
from src.oracle.models.oracle_requests import OracleRequest


class TestProcessRandom(TestCase):

    def test_process_mint_character(self):
        mocked_request = OracleRequest("10", 0, 0, 0, 0, 0, {})
        mocked_request.id = 100

        assert False
