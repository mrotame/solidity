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
def get_oracle(allowed_addresses=None) -> t.Generator[Oracle, Oracle, Oracle]:
    if not allowed_addresses:
        allowed_addresses = []

    with wt.default_chain.connect():
        oracle = Oracle.deploy(allowed_addresses)
        yield oracle


class TestOracle(TestCase):
    def get_min_max_randint(self) -> t.Tuple[int, int]:
        rand_min = randint(0, 1000)
        rand_max = randint(rand_min + 10, rand_min + 1000)
        self.assertGreater(rand_max, rand_min)
        return rand_min, rand_max

    def test_deploy_oracle(self):
        with get_oracle() as oracle:
            self.assertTrue(oracle)

    def test_generate_single_rand_uint_function(self):
        rand_min, rand_max = self.get_min_max_randint()

        with get_oracle() as oracle:
            vrf_caller = VRFCaller.deploy(oracle.address)
            oracle.updateAllowedAddress(vrf_caller.address, True)
            required_wei = oracle.getbaseGasGweiFee() * GWEI
            wt.Account(1).balance = required_wei

            request = vrf_caller.generateSingleRandUint(
                rand_min, rand_max, value=required_wei, from_=wt.Address(1)
            )

            self.assertTrue(request.events)
            self.assertIsInstance(request.events[0], oracle.RequestCreated)
            self.assertIsInstance(request.events[1], oracle.SingleRandUintParams)
            self.assertEqual(request.events[0].requester, vrf_caller.address)
            self.assertEqual(request.events[1].min_num, rand_min)
            self.assertEqual(request.events[1].max_num, rand_max)

    def test_generate_rand_uint_array_function(self):
        rand_min, rand_max = self.get_min_max_randint()
        quantity = randint(1, 20)

        with get_oracle() as oracle:
            vrf_caller = VRFCaller.deploy(oracle.address)
            oracle.updateAllowedAddress(vrf_caller.address, True)
            required_wei = oracle.getbaseGasGweiFee() * GWEI
            wt.Account(1).balance = required_wei

            result = vrf_caller.generateRandUintArray(
                rand_min,
                rand_max,
                quantity,
                from_=wt.Address(1),
                value=required_wei,
            )

            self.assertTrue(result.events)
            self.assertIsInstance(result.events[0], oracle.RequestCreated)
            self.assertIsInstance(result.events[1], oracle.RandUintArrayParams)
            self.assertEqual(result.events[0].requester, vrf_caller.address)
            self.assertEqual(result.events[1].min_num, rand_min)
            self.assertEqual(result.events[1].max_num, rand_max)
            self.assertEqual(result.events[1].quantityRequired, quantity)

    def test_fulfill_request_random_single_unit(self):
        rand_min, rand_max = self.get_min_max_randint()
        rand_num = randint(rand_min, rand_max)

        with get_oracle() as oracle:
            vrf_caller = VRFCaller.deploy(oracle.address)
            oracle.updateAllowedAddress(vrf_caller.address, True)
            required_wei = oracle.getbaseGasGweiFee() * GWEI
            wt.Account(1).balance = required_wei

            request = vrf_caller.generateSingleRandUint(
                rand_min, rand_max, from_=wt.Address(1), value=required_wei
            )

            result = oracle.fulfillSingleRandUintRequest(
                request.events[0].requestId, rand_num
            )

            self.assertEqual(
                vrf_caller.functionCalled(), "fulfillRequestRandUint_singleUint"
            )

            self.assertEqual(vrf_caller.requestId(), request.events[0].requestId)

            self.assertEqual(vrf_caller.msgSender(), oracle.address)

            self.assertEqual(vrf_caller.randomUint(), rand_num)

            self.assertIsInstance(result.events[0], oracle.RequestFulfilled)

            self.assertEqual(result.events[0].requestId, vrf_caller.requestId())

    def test_fulfill_request_random_unit_array(self):
        rand_min, rand_max = self.get_min_max_randint()
        quantity = randint(2, 20)
        rand_num = [randint(rand_min, rand_max) for i in range(quantity)]

        with get_oracle() as oracle:
            vrf_caller = VRFCaller.deploy(oracle.address)
            oracle.updateAllowedAddress(vrf_caller.address, True)
            required_wei = oracle.getbaseGasGweiFee() * GWEI
            wt.Account(1).balance = required_wei

            request = vrf_caller.generateRandUintArray(
                rand_min,
                rand_max,
                quantity,
                from_=wt.Address(1),
                value=required_wei,
            )

            result = oracle.fulfillRandUintArrayRequest(
                request.events[0].requestId, rand_num
            )

            self.assertEqual(
                vrf_caller.functionCalled(), "fulfillRequestRandUint_uintArray"
            )

            for i in range(len(rand_num)):
                self.assertEqual(vrf_caller.randomUints(i), rand_num[i])

            self.assertGreater(len(rand_num), 0)

    def test_transfer_gas(self):
        with get_oracle() as oracle:
            vrf_caller = VRFCaller.deploy(oracle.address)

            oracle.setCallerAddress(vrf_caller.address)
            oracle.updateAllowedAddress(vrf_caller.address, True)

            required_wei = oracle.getbaseGasGweiFee() * GWEI
            oracle.balance = required_wei * 10

            with wt.must_revert():
                request = oracle.generateSingleRandUint(
                    10, 1000, from_=vrf_caller.address
                )

            oracle.transferGas()

            self.assertEqual(vrf_caller.balance, required_wei * 10)

            request = oracle.generateSingleRandUint(
                10, 1000, from_=vrf_caller.address, value=required_wei
            )
