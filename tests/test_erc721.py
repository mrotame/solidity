import typing as t
from random import randint
from unittest import TestCase
from contextlib import contextmanager

import wake.testing as wt

from pytypes.contracts.common.tokens.ERC721 import ERC721
from pytypes.contracts.common.utils.ERC721_receiver import ERC721Receiver


@contextmanager
def get_token() -> t.Generator[ERC721, ERC721, ERC721]:
    with wt.default_chain.connect():
        token = ERC721.deploy("test_nft", "tstn", 0)
        yield token


@contextmanager
def get_token_receiver() -> t.Generator[ERC721, ERC721, ERC721]:
    with wt.default_chain.connect():
        token = ERC721Receiver.deploy()
        yield token


class TestErc721(TestCase):
    def test_constructor(self):
        with get_token() as token:
            self.assertEqual(token.name(), "test_nft")
            self.assertEqual(token.symbol(), "tstn")

    def test_owner_of(self):
        with get_token() as token:
            res = token.mint(wt.Address(1))
            minted_token_id = res.events[0]._tokenId

            self.assertEqual(token.ownerOf(minted_token_id), wt.Address(1))

    def test_mint_token(self):
        to_mint = randint(0, 100)

        with get_token() as token:
            minted_ids = []
            for i in range(to_mint):
                res = token.mint(wt.Address(1))
                minted_ids.append(res.events[0]._tokenId)

            self.assertEqual(
                wt.read_storage_variable(token, "balances", keys=[wt.Address(1)]),
                to_mint,
            )

            self.assertEqual(wt.read_storage_variable(token, "current_supply"), to_mint)

    def test_safe_mint_token(self):
        with get_token() as token:
            token_receiver = ERC721Receiver.deploy()
            token_owner = wt.read_storage_variable(token, "contract_owner")

            mint = token.safeMint_(token_receiver.address, b"test_safe_mint_data")

            self.assertEqual(token.balanceOf(token_receiver.address), 1)
            self.assertEqual(token.total_supply(), 1)
            self.assertEqual(
                token.ownerOf(mint.events[0]._tokenId), token_receiver.address
            )

            self.assertEqual(token_receiver.token_received(), True)
            self.assertEqual(token_receiver.sender(), token.address)
            self.assertEqual(token_receiver.operator(), token_owner)
            self.assertEqual(token_receiver.received_from(), wt.Address(0))
            self.assertEqual(token_receiver.token_id(), mint.events[0]._tokenId)
            self.assertEqual(token_receiver.data(), b"test_safe_mint_data")

    def test_mint_and_safe_mint_token_from_unauthorized_address(self):
        with get_token() as token:
            with wt.must_revert():
                token.mint(wt.Address(1), from_=wt.Address(1))

            with wt.must_revert():
                token.safeMint(wt.Address(1), from_=wt.Address(1))

            self.assertEqual(token.balanceOf(wt.Address(1)), 0)

            self.assertEqual(token.total_supply(), 0)

    def test_transfer_from(self):
        tokens_id = []
        with get_token() as token:
            for _ in range(3):
                res = token.mint(wt.Address(1))
                tokens_id.append(res.events[0]._tokenId)

            token.transferFrom(wt.Address(1), wt.Address(2), tokens_id[0])
            token.transferFrom(
                wt.Address(1), wt.Address(2), tokens_id[1], from_=wt.Address(1)
            )

            with wt.must_revert():
                token.transferFrom(
                    wt.Address(1), wt.Address(2), tokens_id[2], from_=wt.Address(2)
                )

            self.assertEqual(token.total_supply(), 3)
            self.assertEqual(token.balanceOf(wt.Address(1)), 1)
            self.assertEqual(token.balanceOf(wt.Address(2)), 2)

            self.assertEqual(token.ownerOf(tokens_id[0]), wt.Address(2))
            self.assertEqual(token.ownerOf(tokens_id[1]), wt.Address(2))
            self.assertEqual(token.ownerOf(tokens_id[2]), wt.Address(1))

    def test_safe_transfer_from(self):
        with get_token() as token:
            token_receiver = ERC721Receiver.deploy()
            token_owner = wt.read_storage_variable(token, "contract_owner")

            token_id = token.mint(wt.Address(1)).events[0]._tokenId

            token.safeTransferFrom_(
                wt.Address(1),
                token_receiver.address,
                token_id,
                b"test_safe_tranfer_data",
            )

            self.assertEqual(token.balanceOf(token_receiver.address), 1)
            self.assertEqual(token.balanceOf(wt.Address(1)), 0)
            self.assertEqual(token.total_supply(), 1)
            self.assertEqual(token.ownerOf(token_id), token_receiver.address)

            self.assertEqual(token_receiver.token_received(), True)
            self.assertEqual(token_receiver.sender(), token.address)
            self.assertEqual(token_receiver.operator(), token_owner)
            self.assertEqual(token_receiver.received_from(), wt.Address(0))
            self.assertEqual(token_receiver.token_id(), token_id)
            self.assertEqual(token_receiver.data(), b"test_safe_tranfer_data")

    def test_transfer_and_safe_transfer_from_unauthorized_address(self):
        with get_token() as token:
            token_id = token.mint(wt.Address(1)).events[0]._tokenId

            with wt.must_revert():
                token.transferFrom(
                    wt.Address(1), wt.Address(2), token_id, from_=wt.Address(2)
                )

            with wt.must_revert():
                token.safeTransferFrom(
                    wt.Address(1), wt.Address(2), token_id, from_=wt.Address(2)
                )

            with wt.must_revert():
                token.safeTransferFrom_(
                    wt.Address(1),
                    wt.Address(2),
                    token_id,
                    b"test_data",
                    from_=wt.Address(2),
                )

            self.assertEqual(token.balanceOf(wt.Address(1)), 1)
            self.assertEqual(token.ownerOf(token_id), wt.Address(1))

            self.assertEqual(token.balanceOf(wt.Address(2)), 0)

    def test_approve(self):
        pass

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
