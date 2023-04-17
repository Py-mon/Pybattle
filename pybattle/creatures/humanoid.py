from typing import Any

from pybattle.creatures.attributes.reinforcements import Armor, Weapon
from pybattle.creatures.pymon import Pymon


class Humanoid(Pymon):
    """A human or human like creature that is the same as a Pymon but with armor and weapons. Cannot be bred"""

    def __init__(self, stats: dict[str, Any] = {}):
        """
        Args:
            - `'name': str`
            - `'moves': list[Move]`
            - `'trait_amount': int`
            - `'elements': list[ElementReference]`
            - `'ability': Ability`
            - `'item': Item`
            - `'graphics': str`
            - `'starting_level': int`
            - `'weapon': Weapon`
            - `'armor': Armor`
            - `'helmet': Armor`
        """
        super().__init__(stats)

        self.weapon: Weapon | None = stats.get("weapon")
        if self.weapon is not None:
            self.stats[self.weapon.stat].bonus *= self.weapon.mult
            self.stats["speed"].bonus /= self.weapon.speed_decrease_mult

        self.armor: Armor | None = stats.get("armor")
        if self.armor is not None:
            self.stats["defense"].bonus *= self.armor.defense_mult
            self.stats["speed"].bonus /= self.armor.speed_decrease_mult

        self.helmet: Armor | None = stats.get("helmet")
        if self.helmet is not None:
            self.stats["defense"].bonus *= self.helmet.defense_mult
            self.stats["speed"].bonus /= self.helmet.speed_decrease_mult

    @property
    def total_graphics(self) -> str:
        """The combined graphics of the Humanoid"""
        if (
            self.helmet is not None
            and self.weapon is not None
            and self.armor is not None
        ):
            return "\n".join(
                map(
                    "".join,
                    zip(
                        (self.helmet.graphics + self.armor.graphics).splitlines(),
                        self.weapon.graphics.splitlines(),
                    ),
                )
            )
        return self.graphics

    def breed(self, *_, **__) -> None:
        raise AttributeError("Breeding is not allowed for Humanoids.")
