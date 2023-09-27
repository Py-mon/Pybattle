from random import choices
from typing import Callable

from pybattle.types_ import Creature
from dataclasses import dataclass


TRAITS: list["Trait"] = []


@dataclass
class Trait:
    """A quality or characteristic belonging to a creature."""

    name: str
    function: Callable[[Creature], None]

    @classmethod
    def generate(cls, x: int = 2) -> set["Trait"] | None:
        """Generate `x` number of random traits. May have less if it generates the same trait.

        Returns `None` if there are too few traits."""
        if len(TRAITS) >= x:
            traits = set(
                choices(
                    TRAITS,
                    k=x,
                )
            )
            return traits
        else:
            return None

    @staticmethod
    def creases(increases: list[str], decreases: list[str], percent: float = 0.1):
        """Create a function that increases and decreases a User's stats by a percent."""

        def func(user: Creature) -> None:
            for increase in increases:
                user.bonuses[increase] *= percent
            for decrease in decreases:
                user.bonuses[decrease] /= percent

        return func

    def __post_init__(
        self,
    ) -> None:
        TRAITS.append(self)

    def __repr__(self) -> str:
        return type(self).__name__ + ":" + self.name


"""
Evolution
Skins (Shiny)

Aging: Implement an aging system where Pymon's appearance and attributes change as they progress through different lifestages.
Pymon Emotions: Assign emotions or moods to Pymon that can influence their behavior and interactions. '

Dynamic Stat Growth: Implement a more dynamic system where certain stats have a higher growth rate during different life stages'
Stat Specialization: Allow players to choose certain stats to specialize in as their Pymon levels up.'

Stat Decay: Introduce a stat decay mechanic where unused or underutilized stats gradually decrease over time, encouraging players to regularly engage with their Pymon.
Stat-Dependent Evolution Paths: Design multiple evolution paths for each Pymon species, each influenced by different stat distributions. 

"""

Trait("brave", Trait.creases(["attack"], ["speed"]))
Trait("fierce", Trait.creases(["attack"], ["magic"]))
Trait("aggressive", Trait.creases(["attack"], ["defense"]))
Trait("swift", Trait.creases(["attack"], ["energy"]))

Trait("careful", Trait.creases(["defense"], ["speed"]))
Trait("shy", Trait.creases(["defense"], ["magic"]))
Trait("tired", Trait.creases(["defense"], ["energy"]))
Trait("tough", Trait.creases(["defense"], ["attack"]))

Trait("cheerful", Trait.creases(["energy"], ["defense"]))
Trait("courageous", Trait.creases(["energy"], ["magic"]))
Trait("eager", Trait.creases(["energy"], ["speed"]))
Trait("excited", Trait.creases(["energy"], ["attack"]))

Trait("hungry", Trait.creases(["speed"], ["energy"]))
Trait("curious", Trait.creases(["speed"], ["defense"]))
Trait("energetic", Trait.creases(["speed"], ["attack"]))
Trait("adventurous", Trait.creases(["speed"], ["defense"]))

Trait("enchanting", Trait.creases(["magic"], ["defense"]))
Trait("hypnotic", Trait.creases(["magic"], ["energy"]))
Trait("angelic", Trait.creases(["magic"], ["attack"]))
Trait("modest", Trait.creases(["magic"], ["speed"]))
