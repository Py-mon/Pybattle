from .ability import Ability
from src.types_ import Creature


class Item(Ability):
    """A beneficial equip-able object for any creature. """

    def equip(self, to: Creature) -> None:
        """Equip an Item to a Creature."""
        to.item = self
