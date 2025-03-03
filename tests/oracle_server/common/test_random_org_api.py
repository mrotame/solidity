from unittest import TestCase
from random import randint

from oracle.common.random_org_api import RandomOrg
from oracle.models.signed_random import SignedRandom


class TestRandomOrgApi(TestCase):
    rand = RandomOrg()

    def test_get_random_int(self):
        min = randint(0, 10)
        max = randint(100, 200)

        num, signed_item = self.rand.get_random_int(min, max)
        signed_item.save()

        self.assertGreaterEqual(num, min)
        self.assertLessEqual(num, max)

        self.rand.client.verify_signature(signed_item.random, signed_item.signature)

        self.assertIsNotNone(SignedRandom.get(signed_item.id))

    def test_get_random_int_array(self):
        min = randint(0, 10)
        max = randint(100, 200)
        quantity = randint(2, 5)

        nums, signed_item = self.rand.get_random_int_array(quantity, min, max)
        signed_item.save()

        for i in nums:
            self.assertGreaterEqual(i, min)
            self.assertLessEqual(i, max)

        self.assertEqual(len(nums), quantity)

        self.rand.client.verify_signature(signed_item.random, signed_item.signature)

        self.assertIsNotNone(SignedRandom.get(signed_item.id))
