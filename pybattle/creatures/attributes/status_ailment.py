from typing import Callable

from pybattle.creatures.attributes.element import Element
from pybattle.types_ import Attacker, Creature, Defender


class StatusEffect:
    """A negative status effect on a creature."""

    def __init__(
        self,
        element: Element,
        function: Callable[[list[Attacker], list[Defender]], None],
    ) -> None:
        self.element = element
        self.function = function

    def __repr__(self) -> str:
        return type(self).__name__ + ":" + self.function.__name__

    def affect(self, creature: Creature) -> None:
        """Cause a negative effect on a Creature."""
        creature.status_effects.append(self)
