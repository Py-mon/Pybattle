"""A negative status effect on a creature."""

from typing import Callable

from src.types_ import Attacker, Creature, Defender, ElementReference

from .element import Element


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
        return function.__name__.capitalize()

    def affect(self, creature: Creature) -> None:
        """Cause a negative effect on a Creature."""
        creature.status_ailments.append(self)
