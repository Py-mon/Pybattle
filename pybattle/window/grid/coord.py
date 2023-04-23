from typing import Self, Iterator
from collections.abc import Iterable
from pybattle.log.errors import InvalidConvertType


class Coord:
    """
    Represents a 2D coordinate with positive values only, in the format of (y, x) or (row, col). It provides methods for setting and retrieving the coordinates, performing arithmetic operations, and lexicographical sorting.
    """

    def __init__(self, y: int, x: int) -> None:
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
    def _convert(cls, obj) -> Self:
        """Converts an object to a Coord object, either by unpacking a tuple or by creating a Coord object with the same y and x values"""
        if isinstance(obj, Iterable):
            obj = cls(*obj)
        elif isinstance(obj, int):
            obj = cls(obj, obj)
        else:
            raise InvalidConvertType(type(obj), cls)
        return obj

    def __iter__(self) -> Iterator[int]:
        """Allows iterating over the Coord object, returning the (y, x) coordinates as a tuple"""
        return iter(self.coords)

    def __add__(self, other) -> Self:
        """
        Returns a new Coord object resulting from element-wise addition of
        the current Coord object with another Coord object, iterable, or integer.
        """
        other = type(self)._convert(other)
        return type(self)(self.y + other.y, self.x + other.x)

    def __sub__(self, other) -> Self:
        """
        Returns a new Coord object resulting from element-wise subtraction of
        the current Coord object with another Coord object, iterable, or integer.
        """
        other = type(self)._convert(other)
        return type(self)(self.y - other.y, self.x - other.x)

    def __eq__(self, other) -> bool:
        """Compares the current Coord object with another Coord object, iterable, or integer for equality"""
        other = type(self)._convert(other)
        return self.coords == other.coords

    def __lt__(self, other) -> bool:
        """Compares the current Coord object with another Coord object, iterable, or integer for lexicographical sorting"""
        other = type(self)._convert(other)
        return self.coords < other.coords

    def __repr__(self) -> str:
        """Returns a string representation of the Coord object"""
        return f"Coord(y={self.y}, x={self.x})"

    def __hash__(self) -> int:
        """Returns the hash value of the Coord object"""
        return hash(self.coords)
