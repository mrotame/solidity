import typing as t


CHARACTER_CLASSES = ["miner", "lumberjack", "fisherman", "warrior", "merchant"]
SKILL_NAMES = ["Mining", "Wood Cutting", "Fishing", "Fighting", "Trading"]


class CharacterMetadata:
    base_metadata = {
        "name": "Worker",
        "description": "",
    }

    @classmethod
    def build_character_metadata(cls, attributes: t.List[int]) -> t.Dict[str, t.Any]:
        character_class = cls.get_character_class(attributes)

        metadata = {
            **cls.base_metadata,
            "class": character_class,
            "image": cls.get_character_png(character_class),
            "attributes": [],
        }

        for i in range(len(attributes)):
            metadata["attributes"].append(
                {
                    "display_type": "boost_percentage",
                    "trait_type": (
                        SKILL_NAMES[i // 2].capitalize() + " Power"
                        if i % 2 == 0
                        else " Speed"
                    ),
                    "value": attributes[i],
                }
            )

        return metadata

    @classmethod
    def get_character_class(cls, attributes: t.List[int]):
        highest = 0
        highest_index = 0
        current_i = -1

        for i in range(0, len(attributes), 2):
            current_i += 1
            avarage = (attributes[i] + attributes[i + 1]) / 2
            if avarage > highest:
                highest = avarage
                highest_index = current_i

        return CHARACTER_CLASSES[highest_index]

    @classmethod
    def get_character_png(cls, char_class: str):
        return ""
