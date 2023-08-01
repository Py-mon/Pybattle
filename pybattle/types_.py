from collections.abc import Iterable, Sequence
from enum import Enum
from itertools import chain
from typing import TYPE_CHECKING, Any, Self, Sized, TypeAlias, TypeVar, Union

if TYPE_CHECKING:
    from pybattle.creatures.attributes.element import Element
    from pybattle.creatures.humanoid import Humanoid
    from pybattle.creatures.pymon import Pymon


Creature = Union["Pymon", "Humanoid"]
User: TypeAlias = "Humanoid"

ElementReference = Union[str, "Element"]


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


class CardinalDirection(Enum):
    NORTH = 0
    WEST = 1
    EAST = 2
    SOUTH = 3


class Alignment(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2
    MIDDLE = 2

    def align(self, string: str, width: int) -> str:
        if self == Alignment.LEFT:
            return string.ljust(width)
        elif self == Alignment.RIGHT:
            return string.rjust(width)
        elif self == Alignment.CENTER or self == Alignment.MIDDLE:
            return string.center(width)
        return str()


class Thickness(Enum):
    THIN = 0
    THICK = 1
    DOUBLE = 2


JunctionDict = dict[Direction, Thickness]
