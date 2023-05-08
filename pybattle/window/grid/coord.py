from collections.abc import Iterable
from math import sqrt
from typing import Iterator, Self

from pybattle.log.errors import InvalidConvertType


class Coord:
    """Represents a 2D coordinate with positive values only, in the format of (y, x) or (row, col)"""

    def __init__(self, y: int = 0, x: int = 0) -> None:
        self.y = y
        self.x = x

    @property
    def coords(self) -> tuple[int, int]:
        """Returns the current (y, x) coordinates as a tuple"""
        return self.y, self.x

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, to: int):
        self.__x = max(0, to)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, to: int):
        self.__y = max(0, to)

    @classmethod
    def _convert(cls, obj: Self | int | Iterable) -> Self:
        """Tries to convert the object to a Coord object

        Raises InvalidConvertType error on invalid object type"""
        obj_ = None
        if isinstance(obj, Iterable):
            obj_ = cls(*obj)
        elif isinstance(obj, int):
            obj_ = cls(obj, obj)
        else:
            raise InvalidConvertType(type(obj), cls)
        return obj_ or obj

    def __iter__(self) -> Iterator[int]:
        return iter(self.coords)

    def __add__(self, other) -> Self:
        other = type(self)._convert(other)
        return type(self)(self.y + other.y, self.x + other.x)

    def __sub__(self, other) -> Self:
        other = type(self)._convert(other)
        return type(self)(self.y - other.y, self.x - other.x)

    def __eq__(self, other) -> bool:
        other = type(self)._convert(other)
        return self.coords == other.coords

    def __lt__(self, other) -> bool:
        # Lexicographical Sorting
        other = type(self)._convert(other)
        return self.coords < other.coords

    def __repr__(self) -> str:
        return f"Coord(y={self.y}, x={self.x})"

    def __hash__(self) -> int:
        return hash(self.coords)

    def distance(self, other: Self) -> float:
        """Get the distance between one coord and another"""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
