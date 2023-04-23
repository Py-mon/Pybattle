from enum import Enum
from typing import TYPE_CHECKING, TypeAlias, Union, Iterable

if TYPE_CHECKING:
    from pybattle.ansi.colors import ColorType
    from pybattle.creatures.attributes.element import Element
    from pybattle.creatures.humanoid import Humanoid
    from pybattle.creatures.pymon import Pymon
    from pybattle.window.grid.coord import Coord
    from pybattle.window.grid.size import Size
    from pybattle.window.grid.range import RectRange, SelectionRange


Creature = Union["Pymon", "Humanoid"]
Attacker = Creature
Defender = Creature
User: TypeAlias = "Humanoid"

ElementReference = Union[str, "Element"]
CoordReference = Union["Coord", Iterable, int]
SizeReference = Union["Size", CoordReference]

ColorRange = tuple["ColorType", Union["RectRange", "SelectionRange"]]


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __lt__(self, other):
        return self.value < other.value


class Align(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2
    MIDDLE = 2


class Thickness(Enum):
    THIN = 0
    THICK = 1
    DOUBLE = 2


Junction = dict[Direction, Thickness]
f
