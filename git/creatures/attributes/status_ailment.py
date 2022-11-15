from typing import Callable

from .element import Element
from types_ import Attacker, Creature, Defender, ElementReference


class StatusAilment:
    """A negative status effect on a creature."""

    def __init__(
        self,
        element: ElementReference,
        function: Callable[[list[Attacker], list[Defender]], None]
    ) -> None:
        self.element = Element.convert_element_references([element])
        self.function = function
        
    def __repr__(self) -> str:
        return str([name for name, obj in globals().items() if id(obj) == id(self)])

    def affect(self, creature: Creature) -> None:
        """Cause a negative effect on a Creature."""
        creature.status_ailments.append(self)
