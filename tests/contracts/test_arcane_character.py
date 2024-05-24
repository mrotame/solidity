import typing as t
from unittest import TestCase
from contextlib import contextmanager

import wake.testing as wt

from pytypes.contracts.game.characters import ArcaneCharacters


@contextmanager
def get_token() -> t.Generator[ArcaneCharacters, ArcaneCharacters, ArcaneCharacters]:
    with wt.default_chain.connect():
        token = ArcaneCharacters.deploy([])
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
