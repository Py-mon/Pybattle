from typing import TYPE_CHECKING, Union, TypeAlias, Tuple

if TYPE_CHECKING:
    from pybattle.creatures.attributes.element import Element
    from pybattle.creatures.humanoid import Humanoid
    from pybattle.creatures.pymon import Pymon
    from pybattle.window.coord import Coord
    from pybattle.window.range import Size


Creature = Union["Pymon", "Humanoid"]
Attacker = Creature
Defender = Creature
User: TypeAlias = "Humanoid"

ElementReference = Union[str, "Element"]
CoordReference = Union["Coord", Tuple, int]
SizeReference = Union["Size", Tuple, int]

Reference2D = Tuple | int
