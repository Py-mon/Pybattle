from collections.abc import Iterable
from copy import copy
from math import sqrt
from typing import Iterator, Optional, Self

from pybattle.log.errors import InvalidConvertType


class Coord:
    """Represents a 2D coordinate with positive values only, in the format of (y, x) or (row, col)"""

    # __instances = {}

    # def __new__(cls, *args):
    #     # Dont create another instance if its already been created
    #     key = (cls, args)
    #     if key not in cls.__instances:
    #         instance = super().__new__(cls)
    #         instance.__init = True
    #         return instance

    #     instance = cls.__instances[key]
    #     instance.__init = False
    #     return cls.__instances[key]

    def __init__(self, y: int, x: int) -> None:
        # if not self.__init:
        #     return

        self.y = y
        self.x = x

        # # Stores a copy in the instances so it does have to recreate it
        # self._copy = copy(self)

        # key = (self.__class__, (y, x))
        # self.__class__.__instances[key] = self._copy

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
    def _convert(cls, obj: Self | int) -> Self:
        """Tries to convert the object to a Coord object

        Raises InvalidConvertType error on invalid object type"""
        if isinstance(obj, cls):
            return obj
        elif isinstance(obj, int):
            return cls(obj, obj)
        raise InvalidConvertType(type(obj), cls)

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
