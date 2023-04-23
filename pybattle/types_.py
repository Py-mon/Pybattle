from enum import Enum
from typing import TYPE_CHECKING, TypeAlias, Union, Iterable, Self, Any

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

    def reverse(self) -> Self:
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.LEFT
        return self


class Align(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2
    MIDDLE = 2


class Thickness(Enum):
    THIN = 0
    THICK = 1
    DOUBLE = 2


JunctionDict = dict[Direction, Thickness]


def is_junction(conjunction: Any) -> bool:
    """Check if x is a junction (dict)"""
    return isinstance(conjunction, dict)


def is_nested(lst: list | list[list]) -> bool:
    """Check if a list is nested"""
    return len(lst) > 0 and isinstance(lst[0], list)


def nested_len(lst: list | list[list]) -> int:
    """Get the max nested length of a list. If not nested returns the length."""
    if is_nested(lst):
        return max([len(row) for row in lst] + [0])
    return len(lst)
