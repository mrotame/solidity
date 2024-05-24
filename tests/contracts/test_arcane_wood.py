import typing as t
from random import randint
from unittest import TestCase
from contextlib import contextmanager

import wake.testing as wt

from pytypes.contracts.game.ArcaneWood import ArcaneWood


@contextmanager
def get_token() -> t.Generator[ArcaneWood, ArcaneWood, ArcaneWood]:
    with wt.default_chain.connect():
        token = ArcaneWood.deploy([])
        yield token


class TestArcaneWood(TestCase):
    def get_contractOwner(self, token: ArcaneWood) -> wt.Address:
        return wt.read_storage_variable(token, "contractOwner")

    def test_constructor(self):
        with get_token() as token:
            max_supply = wt.read_storage_variable(token, "max_supply")

            self.assertEqual(token.name(), "Arcane Wood")
            self.assertEqual(token.symbol(), "ARW")
            self.assertEqual(token.decimals(), 18)
            self.assertEqual(max_supply, 0)

    def test_transfer_from_fees(self):
        with get_token() as token:
            token_amount = randint(1000, 10000)
            percentage = wt.read_storage_variable(token, "tax_fee_percent")

            tax_amount = int((token_amount * percentage) / 100)

            token.mint(wt.Address(1), token_amount)

            token.transfer(wt.Address(2), token_amount, from_=wt.Address(1))

            self.assertEqual(token.balanceOf(wt.Address(2)), token_amount - tax_amount)
            self.assertEqual(token.balanceOf(wt.Address(1)), 0)
            self.assertEqual(token.balanceOf(self.get_contractOwner(token)), tax_amount)

    def test_transfer_from_fees_admin(self):
        with get_token() as token:
            token.update_admin_address(wt.Address(1), True)

            token_amount = randint(1000, 10000)
            token.mint(wt.Address(1), token_amount)

            token.transfer(wt.Address(2), token_amount, from_=wt.Address(1))

            self.assertEqual(token.balanceOf(wt.Address(2)), token_amount)
            self.assertEqual(token.balanceOf(self.get_contractOwner(token)), 0)

    def test_transfer_from_fees_ex_admin(self):
        with get_token() as token:
            token.update_admin_address(wt.Address(1), True)
            token.update_admin_address(wt.Address(1), False)

            token_amount = randint(1000, 10000)
            percentage = wt.read_storage_variable(token, "tax_fee_percent")
            tax_amount = int((token_amount * percentage) / 100)

            token.mint(wt.Address(1), token_amount)

            token.transfer(wt.Address(2), token_amount, from_=wt.Address(1))

            self.assertEqual(token.balanceOf(wt.Address(2)), token_amount - tax_amount)
            self.assertEqual(token.balanceOf(self.get_contractOwner(token)), tax_amount)
