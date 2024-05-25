import typing as t
from random import randint
from unittest import TestCase
from contextlib import contextmanager

import wake.testing as wt

from pytypes.contracts.oracle.Oracle import Oracle

from pytypes.contracts.mock.VRFCaller import VRFCaller

WEI = 1
GWEI = 1000000000


@contextmanager
def get_token() -> t.Generator[Oracle, Oracle, Oracle]:
    with wt.default_chain.connect():
        token = Oracle.deploy()
        yield token


class TestOracle(TestCase):
    def get_min_max_randint(self) -> t.Tuple[int, int]:
        rand_min = randint(0, 1000)
        rand_max = randint(rand_min + 10, rand_min + 1000)
        self.assertGreater(rand_max, rand_min)
        return rand_min, rand_max

    def test_deploy_oracle(self):
        with get_token() as token:
            self.assertTrue(token)

    def test_generate_single_rand_uint_function(self):
        rand_min, rand_max = self.get_min_max_randint()

        with get_token() as token:
            vrf_caller = VRFCaller.deploy(token.address)
            result = token.generateRandUint(
                rand_min, rand_max, from_=vrf_caller.address
            )

            self.assertTrue(result.events)
            self.assertIsInstance(result.events[0], token.RequestCreated)
            self.assertIsInstance(result.events[1], token.RandUintParams)
            self.assertEqual(result.events[0].requester, vrf_caller.address)
            self.assertEqual(result.events[1].min_num, rand_min)
            self.assertEqual(result.events[1].max_num, rand_max)

    def test_generate_rand_uint_array_function(self):
        rand_min, rand_max = self.get_min_max_randint()
        quantity = randint(1, 20)

        with get_token() as token:
            vrf_caller = VRFCaller.deploy(token.address)
            result = token.generateRandUint_(
                rand_min, rand_max, quantity, from_=vrf_caller.address
            )

            self.assertTrue(result.events)
            self.assertIsInstance(result.events[0], token.RequestCreated)
            self.assertIsInstance(result.events[1], token.RandUintParams_)
            self.assertEqual(result.events[0].requester, vrf_caller.address)
            self.assertEqual(result.events[1].min_num, rand_min)
            self.assertEqual(result.events[1].max_num, rand_max)
            self.assertEqual(result.events[1].quantityRequired, quantity)

    def test_fulfill_request_random_single_unit(self):
        rand_min, rand_max = self.get_min_max_randint()
        rand_num = randint(rand_min, rand_max)

        with get_token() as token:
            vrf_caller = VRFCaller.deploy(token.address)

            request = token.generateRandUint(
                rand_min, rand_max, from_=vrf_caller.address
            )

            result = token.fulfillRandUintRequest(request.events[0].requestId, rand_num)

            self.assertEqual(
                vrf_caller.functionCalled(), "fulfillRequestRandUint_singleUint"
            )

            self.assertEqual(vrf_caller.requestId(), request.events[0].requestId)

            self.assertEqual(vrf_caller.msgSender(), token.address)

            self.assertEqual(vrf_caller.randomUint(), rand_num)

            self.assertIsInstance(result.events[0], token.RequestFulfilled)

            self.assertEqual(result.events[0].requestId, vrf_caller.requestId())

    def test_fulfill_request_random_unit_array(self):
        rand_min, rand_max = self.get_min_max_randint()
        quantity = randint(1, 20)
        rand_num = [randint(rand_min, rand_max) for i in range(quantity)]

        with get_token() as token:
            vrf_caller = VRFCaller.deploy(token.address)

            request = token.generateRandUint_(
                rand_min, rand_max, quantity, from_=vrf_caller.address
            )

            result = token.fulfillRandUintRequest_(
                request.events[0].requestId, rand_num
            )

            self.assertEqual(
                vrf_caller.functionCalled(), "fulfillRequestRandUint_uintArray"
            )

            for i in range(len(rand_num)):
                self.assertEqual(vrf_caller.randomUints(i), rand_num[i])

            self.assertGreater(i, 0)

    def test_last_execution_cost(self):
        rand_min, rand_max = self.get_min_max_randint()
        rand_num = randint(rand_min, rand_max)

        with get_token() as token:
            vrf_caller = VRFCaller.deploy(token.address)
            request = token.generateRandUint(
                rand_min, rand_max, from_=vrf_caller.address
            )

            result = token.fulfillRandUintRequest(request.events[0].requestId, rand_num)

            with wt.must_revert():
                token.generateRandUint(rand_min, rand_max, from_=vrf_caller.address)

    def test_pay_for_last_execution(self):
        pass

    def test_fullfill_authorization(self):
        pass
