from random import choices
from typing import Callable

from source.types_ import Creature


class Trait:
    """A quality or characteristic belonging to a creature."""
    traits: list["Trait"] = []

    @classmethod
    def generate(cls, x: int = 2) -> set["Trait"] | None:
        """Generate `x` number of random traits. May have less if it generates the same trait. 

        Returns `None` if there are too few traits."""
        if len(cls.traits) >= x:
            traits = set(choices(
                cls.traits,
                k=x,
            ))
            return traits
        else:
            return None

    @staticmethod
    def creases(increases: list[str], decreases: list[str], percent: float = .1):
        """Create a function that increases and decreases a User's stats by a percent."""
        def func(user: Creature) -> None:
            for increase in increases:
                user.stats[increase].bonus *= percent
            for decrease in decreases:
                user.stats[decrease].bonus /= percent
        return func

    def __init__(
        self,
        name: str,
        function: Callable[[Creature], None],
    ) -> None:
        self.name = name
        self.function = function

        Trait.traits.append(self)

    def __repr__(self) -> str:
        return self.name


Trait('brave', Trait.creases(['attack'], ['speed']))
Trait('fierce', Trait.creases(['attack'], ['magic']))
Trait('aggressive', Trait.creases(['attack'], ['defense']))
Trait('swift', Trait.creases(['attack'], ['energy']))

Trait('careful', Trait.creases(['defense'], ['speed']))
Trait('shy', Trait.creases(['defense'], ['magic']))
Trait('tired', Trait.creases(['defense'], ['energy']))
Trait('tough', Trait.creases(['defense'], ['attack']))

Trait('cheerful', Trait.creases(['energy'], ['defense']))
Trait('courageous', Trait.creases(['energy'], ['magic']))
Trait('eager', Trait.creases(['energy'], ['speed']))
Trait('excited', Trait.creases(['energy'], ['attack']))

Trait('hungry', Trait.creases(['speed'], ['energy']))
Trait('curious', Trait.creases(['speed'], ['defense']))
Trait('energetic', Trait.creases(['speed'], ['attack']))
Trait('adventurous', Trait.creases(['speed'], ['defense']))

Trait('enchanting', Trait.creases(['magic'], ['defense']))
Trait('hypnotic', Trait.creases(['magic'], ['energy']))
Trait('angelic', Trait.creases(['magic'], ['attack']))
Trait('modest', Trait.creases(['magic'], ['speed']))
