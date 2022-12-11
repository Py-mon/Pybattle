from typing import TYPE_CHECKING, Union, TypeAlias

if TYPE_CHECKING:
    from src.creatures.attributes.element import Element
    from src.creatures.humanoid import Humanoid
    from src.creatures.pymon import Pymon
    from src.window.coord import Coord
    from src.window.size import Size


Creature = Union["Pymon", "Humanoid"]
Attacker = Creature
Defender = Creature
User: TypeAlias = "Humanoid"

ElementReference = Union[str, "Element"]
CoordReference = Union["Coord", tuple, int]
SizeReference = Union["Size", tuple, int]
