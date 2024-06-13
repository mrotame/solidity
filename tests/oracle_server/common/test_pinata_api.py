from unittest import TestCase
from uuid import uuid4

from src.oracle.common.pinata_api import PinataApi


class TestPinataApi(TestCase):
    pinata_api = PinataApi()

    def test_check_auth(self):
        response = self.pinata_api.check_auth()

        self.assertEqual(response.status_code, 200)

    def test_pin_json(self):
        seed = str(uuid4().hex)
        tags = {"testing": "true"}
        options = {"cidVersion": 2, "testing": "true"}
        test_json = {
            "seed": seed,
            "pinned_by": "unittest",
        }
        response = self.pinata_api.pin_json(
            json_data=test_json,
            file_name=f"unittest_{seed}",
            tags=tags,
            options=options,
        )

        self.assertEqual(response.status_code, 200)
