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
def get_token(allowed_addresses=None) -> t.Generator[Oracle, Oracle, Oracle]:
    if not allowed_addresses:
        allowed_addresses = []

    with wt.default_chain.connect():
        token = Oracle.deploy(allowed_addresses)
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
            token.updateAllowedAddress(vrf_caller.address, True)

            result = token.generateSingleRandUint(
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
            token.updateAllowedAddress(vrf_caller.address, True)

            result = token.generateRandUintArray(
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
            token.updateAllowedAddress(vrf_caller.address, True)

            request = token.generateSingleRandUint(
                rand_min, rand_max, from_=vrf_caller.address
            )

            result = token.fulfillSingleRandUintRequest(
                request.events[0].requestId, rand_num
            )

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
            token.updateAllowedAddress(vrf_caller.address, True)

            request = token.generateRandUintArray(
                rand_min, rand_max, quantity, from_=vrf_caller.address
            )

            result = token.fulfillRandUintArrayRequest(
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
            token.updateAllowedAddress(vrf_caller.address, True)

            request = token.generateSingleRandUint(
                rand_min, rand_max, from_=vrf_caller.address
            )

            result = token.fulfillSingleRandUintRequest(
                request.events[0].requestId, rand_num
            )

            with wt.must_revert():
                token.generateSingleRandUint(
                    rand_min, rand_max, from_=vrf_caller.address
                )

            self.assertEqual(
                result.events[0].callbackCost,
                token.getlastExecutionCost(
                    vrf_caller.address, token.RequestTypes.RANDUINT_SINGLE
                ),
            )

            self.assertGreaterEqual(result.events[0].callbackCost, result.gas_used)

    def test_pay_for_last_execution(self):
        rand_min, rand_max = self.get_min_max_randint()
        rand_num = randint(rand_min, rand_max)

        extra_gwei = randint(0, 1000) * GWEI

        with get_token() as token:
            vrf_caller = VRFCaller.deploy(token.address)
            token.updateAllowedAddress(vrf_caller.address, True)

            request = token.generateSingleRandUint(
                rand_min, rand_max, from_=vrf_caller.address
            )

            result = token.fulfillSingleRandUintRequest(
                request.events[0].requestId, rand_num
            )

            spent = result.events[0].callbackCost
            vrf_caller.balance = spent * GWEI + extra_gwei

            request = token.generateSingleRandUint(
                rand_min, rand_max, from_=vrf_caller.address, value=spent * GWEI
            )

            with wt.must_revert():
                token.generateSingleRandUint(
                    rand_min, rand_max, from_=vrf_caller.address
                )

            self.assertEqual(vrf_caller.balance, extra_gwei)

    def test_fulfill_request_payment_and_auth(self):
        rand_min, rand_max = self.get_min_max_randint()
        rand_num = randint(rand_min, rand_max)
        rand_nums = [randint(rand_min, rand_max) for i in range(10)]

        extra_gwei = randint(0, 1000) * GWEI

        with get_token() as token:
            vrf_caller = VRFCaller.deploy(token.address)
            token.updateAllowedAddress(vrf_caller.address, True)

            request = token.generateSingleRandUint(
                rand_min, rand_max, from_=vrf_caller.address
            )

            token.fulfillSingleRandUintRequest(request.events[0].requestId, rand_num)

            request2 = token.generateRandUintArray(
                rand_min, rand_max, len(rand_nums), from_=vrf_caller.address
            )

            token.fulfillRandUintArrayRequest(request2.events[0].requestId, rand_nums)

            with wt.must_revert():
                token.generateSingleRandUint(
                    rand_min, rand_max, from_=vrf_caller.address
                )

            with wt.must_revert():
                token.generateRandUintArray(
                    rand_min, rand_max, 10, from_=vrf_caller.address
                )

            with wt.must_revert():
                token.generateSingleRandUint(rand_min, rand_max, from_=wt.Address(1))

            token.generateSingleRandUint(rand_min, rand_max)
