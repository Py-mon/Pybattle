from typing import TYPE_CHECKING, Union, TypeAlias, Type, Tuple

if TYPE_CHECKING:
    from pybattle.creatures.attributes.element import Element
    from pybattle.creatures.humanoid import Humanoid
    from pybattle.creatures.pymon import Pymon
    from pybattle.matrix.coord import Coord, Size


Creature = Union["Pymon", "Humanoid"]
Attacker = Creature
Defender = Creature
User: TypeAlias = "Humanoid"

ElementReference = Union[str, "Element"]
CoordReference = Union["Coord", tuple, int]
SizeReference = Union["Size", tuple, int]
