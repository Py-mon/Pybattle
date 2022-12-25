from typing import TYPE_CHECKING, TypeAlias, Union

if TYPE_CHECKING:
    from pybattle.creatures.attributes.element import Element
    from pybattle.creatures.humanoid import Humanoid
    from pybattle.creatures.pymon import Pymon
    from pybattle.window.coord import Coord
    from pybattle.window.size import Size
    from pybattle.window.matrix import Matrix


Creature = Union["Pymon", "Humanoid"]
Attacker = Creature
Defender = Creature
User: TypeAlias = "Humanoid"

ElementReference = Union[str, "Element"]
CoordReference = Union["Coord", tuple, int]
SizeReference = Union["Size", tuple, int]
MatrixReference = Union["Matrix", str, list, SizeReference, list, list[list]]

Reference2D = tuple | int
