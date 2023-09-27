from typing import Callable
from dataclasses import dataclass

from pybattle.creatures.attributes.element import Element
from pybattle.types_ import Attacker, Creature, Defender


@dataclass
class StatusEffect:
    """A negative status effect on a creature."""

    name: str
    element: Element
    function: Callable[[list[Attacker], list[Defender]], None]

    def __repr__(self) -> str:
        return type(self).__name__ + ":" + self.name

    def affect(self, creature: Creature) -> None:
        """Cause a negative effect on a Creature."""
        creature.status_effects.append(self)
