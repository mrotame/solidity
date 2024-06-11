import typing as t
from random import randint

from unittest import TestCase

from src.oracle.common.characters_metadata import CharacterMetadata, CHARACTER_CLASSES


class TestCharacterMetadata(TestCase):

    @property
    def attributes(self) -> t.List[int]:
        return [randint(0, 100) for i in range(10)]

    def test_get_character_class(self):
        attributes_1 = [
            [100, 100, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 100, 100, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 100, 100, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 100, 100, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 100, 100],
        ]
        attributes_2 = [
            [70, 50, 29, 29, 29, 29, 29, 29, 29, 29],
            [29, 29, 70, 50, 29, 29, 29, 29, 29, 29],
            [29, 29, 29, 29, 70, 50, 29, 29, 29, 29],
            [29, 29, 29, 29, 29, 29, 70, 50, 29, 29],
            [29, 29, 29, 29, 29, 29, 29, 29, 70, 50],
        ]

        for i in range(len(attributes_1)):
            self.assertEqual(
                CharacterMetadata.get_character_class(attributes_1[i]),
                CHARACTER_CLASSES[i],
            )

        for i in range(len(attributes_2)):
            self.assertEqual(
                CharacterMetadata.get_character_class(attributes_1[i]),
                CHARACTER_CLASSES[i],
            )

    def test_build_character_metadata(self):
        attributes = self.attributes

        metadata = CharacterMetadata.build_character_metadata(attributes)

        for i in range(len(metadata["attributes"])):
            self.assertEqual(metadata["attributes"][i]["value"], attributes[i])

            if i % 2 == 0:
                self.assertIn(" Power", metadata["attributes"][i]["trait_type"])
            else:
                self.assertIn(" Speed", metadata["attributes"][i]["trait_type"])
