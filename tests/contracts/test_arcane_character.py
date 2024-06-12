import typing as t
from unittest import TestCase
from contextlib import contextmanager

import wake.testing as wt

from pytypes.contracts.game.characters import ArcaneCharacters
from pytypes.contracts.game.ArcaneGold import ArcaneGold
from pytypes.contracts.oracle.Oracle import Oracle


@contextmanager
def get_token() -> t.Generator[ArcaneCharacters, ArcaneCharacters, ArcaneCharacters]:
    with wt.default_chain.connect():
        token = ArcaneCharacters.deploy(wt.Address(1), wt.Address(2), [])
        yield token


class TestArcaneCharacters(TestCase):
    def get_contractOwner(self, token: ArcaneCharacters) -> wt.Address:
        return wt.read_storage_variable(token, "contractOwner")

    def test_constructor(self):
        with get_token() as token:
            max_supply = wt.read_storage_variable(token, "max_supply")

            self.assertEqual(token.name(), "Arcane Characters")
            self.assertEqual(token.symbol(), "ARCH")
            self.assertEqual(max_supply, 0)

    def test_get_oracle_address(self):
        with get_token() as token:
            self.assertEqual(token.getOracleAddress(), wt.Address(1))

    def test_update_oracle_address(self):
        with get_token() as token:
            token.updateOracleAddress(wt.Address(500))
            self.assertEqual(token.getOracleAddress(), wt.Address(500))

            with wt.must_revert():
                token.updateOracleAddress(wt.Address(1), from_=wt.Address(1))

    def test_get_arcane_gold_address(self):
        with get_token() as token:
            self.assertEqual(token.getArcaneGoldAddress(), wt.Address(1))

    def test_update_arcane_gold_address(self):
        with get_token() as token:
            token.updateArcaneGoldAddress(wt.Address(500))
            self.assertEqual(token.getArcaneGoldAddress(), wt.Address(500))

            with wt.must_revert():
                token.updateArcaneGoldAddress(wt.Address(1), from_=wt.Address(1))

    def test_request_mint_character_without_paying(self):
        with get_token() as token:
            oracle: Oracle = Oracle.deploy([token.address])
            arcaneGold: ArcaneGold = ArcaneGold.deploy([token.address])
            arcaneGold.mint(wt.Address(1), token.goldRequiredToMint())
            token.updateArcaneGoldAddress(arcaneGold.address)
            token.updateOracleAddress(oracle.address)

            with wt.must_revert():
                token.requestMint(from_=wt.Address(1))

    def test_request_mint_character_without_gold(self):
        with get_token() as token:
            oracle: Oracle = Oracle.deploy([token.address])
            wt.Account(1).balance = oracle.getbaseGasGweiFee()

            arcaneGold: ArcaneGold = ArcaneGold.deploy([token.address])
            token.updateArcaneGoldAddress(arcaneGold.address)
            token.updateOracleAddress(oracle.address)

            with wt.must_revert():
                token.requestMint(from_=wt.Address(1), value=oracle.getbaseGasGweiFee())

    def test_request_mint_character(self):
        with get_token() as token:
            oracle: Oracle = Oracle.deploy([token.address])
            wt.Account(1).balance = oracle.getbaseGasGweiFee()
            arcaneGold: ArcaneGold = ArcaneGold.deploy([token.address])
            arcaneGold.mint(wt.Address(1), token.goldRequiredToMint())
            token.updateArcaneGoldAddress(arcaneGold.address)
            token.updateOracleAddress(oracle.address)

            token.requestMint(from_=wt.Address(1), value=oracle.getbaseGasGweiFee())

    def test_fulfill_character_mint_request(self):
        with get_token() as token:
            pass
