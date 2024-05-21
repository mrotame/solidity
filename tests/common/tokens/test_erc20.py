import typing as t
from random import randint
from unittest import TestCase
from contextlib import contextmanager

import wake.testing as wt

from pytypes.contracts.common.tokens.ERC20 import ERC20


@contextmanager
def get_token() -> t.Generator[ERC20, ERC20, ERC20]:
    with wt.default_chain.connect():
        token = ERC20.deploy("test_coin", "tstc", 18, 0)
        yield token


class TestErc20(TestCase):
    def test_constructor(self):
        with get_token() as token:

            self.assertEqual(token.name(), "test_coin")
            self.assertEqual(token.symbol(), "tstc")
            self.assertEqual(token.decimals(), 18)

    def test_get_balance(self):
        with get_token() as token:
            token_amount = randint(100, 10000)
            wt.write_storage_variable(
                token, "balances", token_amount, keys=[wt.Address(1)]
            )

            self.assertEqual(token.balanceOf(wt.Address(1)), token_amount)

    def test_transfer_successful(self):
        with get_token() as token:
            token_amount = randint(100, 10000)
            wt.write_storage_variable(
                token, "balances", token_amount, keys=[wt.Address(1)]
            )

            token.transfer(from_=wt.Address(1), _to=wt.Address(2), _value=token_amount)

            self.assertEqual(token.balanceOf(wt.Address(1)), 0)

            self.assertEqual(token.balanceOf(wt.Address(2)), token_amount)

    def test_transfer_without_balance(self):
        with get_token() as token:
            token_amount = randint(100, 10000)
            wt.write_storage_variable(
                token, "balances", token_amount, keys=[wt.Address(1)]
            )

            try:
                token.transfer(
                    from_=wt.Address(1), _to=wt.Address(2), _value=token_amount + 1
                )

            except wt.TransactionRevertedError:
                pass

            self.assertEqual(token.balanceOf(wt.Address(1)), token_amount)

            self.assertEqual(token.balanceOf(wt.Address(2)), 0)

    def test_transfer_from_without_allowance(self):
        with get_token() as token:
            token_amount = randint(100, 10000)
            wt.write_storage_variable(
                token, "balances", token_amount, keys=[wt.Address(1)]
            )

            try:
                token.transferFrom(
                    wt.Address(1), wt.Address(2), token_amount, from_=wt.Address(2)
                )

            except wt.TransactionRevertedError:
                pass

            self.assertEqual(token.balanceOf(wt.Address(1)), token_amount)

            self.assertEqual(token.balanceOf(wt.Address(2)), 0)

    def test_allowance(self):
        with get_token() as token:
            token_amount = randint(100, 10000)

            token.approve(wt.Address(2), token_amount, from_=wt.Address(1))

            self.assertEqual(
                token.allowance(wt.Address(1), wt.Address(2)), token_amount
            )

            self.assertEqual(token.allowance(wt.Address(2), wt.Address(1)), 0)

    def test_transfer_from_with_allowance(self):
        with get_token() as token:
            token_half_amount = randint(100, 10000)
            token_amount = token_half_amount * 2

            token.mint(wt.Address(1), token_amount)
            token.mint(wt.Address(3), token_amount)

            token.approve(wt.Address(2), token_amount, from_=wt.Address(1))
            token.approve(wt.Address(2), token_amount, from_=wt.Address(3))

            token.transferFrom(
                wt.Address(1), wt.Address(4), token_half_amount, from_=wt.Address(2)
            )
            token.transferFrom(
                wt.Address(3), wt.Address(0), token_amount, from_=wt.Address(2)
            )

            with wt.must_revert():
                token.transferFrom(
                    wt.Address(3), wt.Address(0), token_amount, from_=wt.Address(2)
                )

            self.assertEqual(
                token.allowance(wt.Address(1), wt.Address(2)), token_half_amount
            )
            self.assertEqual(token.allowance(wt.Address(3), wt.Address(2)), 0)

            self.assertEqual(token.totalSupply(), token_amount)

            self.assertEqual(token.balanceOf(wt.Address(1)), token_half_amount)

            self.assertEqual(token.balanceOf(wt.Address(3)), 0)

            self.assertEqual(token.balanceOf(wt.Address(4)), token_half_amount)

    def test_mint_token(self):
        with get_token() as token:
            token_amount = randint(100, 10000)

            token.mint(wt.Address(1), token_amount)
            token.mint(wt.Address(2), token_amount)

            with wt.must_revert():
                token.mint(wt.Address(3), token_amount, from_=wt.Address(3))

            self.assertEqual(token.totalSupply(), token_amount * 2)

            self.assertEqual(token.balanceOf(wt.Address(1)), token_amount)

            self.assertEqual(token.balanceOf(wt.Address(2)), token_amount)

            self.assertEqual(token.balanceOf(wt.Address(3)), 0)

    def test_burn_token(self):
        with get_token() as token:
            token_half_amount = randint(100, 10000)
            token_amount = token_half_amount * 2

            token.mint(wt.Address(1), token_amount)
            token.mint(wt.Address(2), token_amount)

            token.burn(wt.Address(1), token_half_amount)
            token.burn(wt.Address(2), token_half_amount)

            self.assertEqual(token.totalSupply(), token_amount)

            self.assertEqual(token.balanceOf(wt.Address(1)), token_half_amount)

            self.assertEqual(token.balanceOf(wt.Address(2)), token_half_amount)

    def test_admin_address(self):
        with get_token() as token:

            self.assertFalse(token.is_admin(wt.Address(randint(0, 100))))

            token.update_admin_address(wt.Address(1), True)
            token.update_admin_address(wt.Address(2), True)
            token.update_admin_address(wt.Address(2), False)

            with wt.must_revert():
                token.update_admin_address(wt.Address(3), True, from_=wt.Address(3))
                token.update_admin_address(wt.Address(1), False, from_=wt.Address(1))

            self.assertTrue(token.is_admin(wt.Address(1)))
            self.assertFalse(token.is_admin(wt.Address(2)))
            self.assertFalse(token.is_admin(wt.Address(3)))

    def test_mint_from_admin(self):
        with get_token() as token:
            token_amount = randint(100, 10000)

            token.update_admin_address(wt.Address(2), True)
            token.update_admin_address(wt.Address(4), True)
            token.update_admin_address(wt.Address(4), False)

            token.mint(wt.Address(1), token_amount, from_=wt.Address(2))
            token.mint(wt.Address(2), token_amount, from_=wt.Address(2))

            with wt.must_revert():
                token.mint(wt.Address(3), token_amount, from_=wt.Address(3))
                token.mint(wt.Address(4), token_amount, from_=wt.Address(4))

            self.assertEqual(token.totalSupply(), token_amount * 2)

            self.assertEqual(token.balanceOf(wt.Address(1)), token_amount)
            self.assertEqual(token.balanceOf(wt.Address(2)), token_amount)
            self.assertEqual(token.balanceOf(wt.Address(3)), 0)
            self.assertEqual(token.balanceOf(wt.Address(4)), 0)

    def test_burn_from_admin(self):
        with get_token() as token:
            token_half_amount = randint(100, 10000)
            token_amount = token_half_amount * 2

            token.update_admin_address(wt.Address(2), True)
            token.update_admin_address(wt.Address(4), True)
            token.update_admin_address(wt.Address(4), False)

            for i in range(4):
                token.mint(wt.Address(i + 1), token_amount)

            token.burn(wt.Address(1), token_half_amount, from_=wt.Address(2))
            token.burn(wt.Address(2), token_amount, from_=wt.Address(2))
            token.burn(wt.Address(3), token_half_amount, from_=wt.Address(3))

            with wt.must_revert():
                token.burn(wt.Address(1), token_half_amount, from_=wt.Address(3))
                token.burn(wt.Address(1), token_half_amount, from_=wt.Address(4))

            self.assertEqual(token.totalSupply(), token_half_amount * 4)

            self.assertEqual(token.balanceOf(wt.Address(1)), token_half_amount)
            self.assertEqual(token.balanceOf(wt.Address(2)), 0)
            self.assertEqual(token.balanceOf(wt.Address(3)), token_half_amount)

    def test_max_supply(self):
        max_amount = randint(100, 10000)
        with wt.default_chain.connect():
            token = ERC20.deploy("test_coin", "tstc", 18, max_amount)

            with wt.must_revert():
                token.mint(wt.Address(1), max_amount + 1)

            self.assertEqual(token.balanceOf(wt.Address(1)), 0)
