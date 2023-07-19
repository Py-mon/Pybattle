from collections.abc import Iterable
from math import sqrt
from typing import Iterable, NamedTuple, Optional, Self

from pybattle.log.errors import NegativeError
from pybattle.types_ import nested_len


class _Point(NamedTuple):
    """Immutable 2D point in the format of (y, x) or (row, col)"""

    y: int
    x: int

    @classmethod
    def _convert(cls, obj: Iterable[int] | Self | int) -> Iterable[int] | Self:
        if not isinstance(obj, int):
            return obj
        return obj, obj

    def __add__(self, __other: Iterable[int] | Self | int) -> Self:
        y, x = type(self)._convert(__other)
        return type(self)(self.y + y, self.x + x)

    def __sub__(self, __other: Iterable[int] | Self | int) -> Self:
        y, x = type(self)._convert(__other)
        return type(self)(self.y - y, self.x - x)

    def __mul__(self, __other: Iterable[int] | Self | int) -> Self:
        y, x = type(self)._convert(__other)
        return type(self)(self.y * y, self.x * x)

    def __pow__(self, __other: Iterable[int] | Self | int) -> Self:
        y, x = type(self)._convert(__other)
        return type(self)(self.y**y, self.x**x)

    def __floordiv__(self, __other: Iterable[int] | Self | int) -> Self:
        y, x = type(self)._convert(__other)
        return type(self)(self.y // y, self.x // x)


class Coord(_Point):
    """Immutable 2D coordinate with positive values only, in the format of (y, x) or (row, col)"""

    def __init__(self, y: int, x: int):
        if y < 0 or x < 0:
            raise NegativeError({"y": y, "x": x}, type(self))

    @property
    def coords(self) -> tuple[int, int]:
        """Returns the current (y, x) coordinates as a tuple"""
        return tuple(self)

    def __lt__(self, __other) -> bool:
        """Lexicographical Sorting"""
        return self.coords < tuple(type(self)._convert(__other))


class Size(_Point):
    """Immutable (height, width) with positive values only, representing the ending coordinate of a object"""

    def rect_range(self, start: Optional[Coord] = None) -> list[Coord]:
        start = start or Coord(0, 0)
        return [
            Coord(y, x)
            for y in range(start.y, self.y + 1)
            for x in range(start.x, self.x + 1)
        ]

    @property
    def center(self) -> Self:
        """The center point of the Size"""
        return self // 2

    @classmethod
    def from_str(cls, string: str) -> Self:
        """Get the Size of a str"""
        return Size(
            string.removeprefix("\n").count("\n"), nested_len(string.splitlines())
        )

    @classmethod
    def from_list(cls, lst: list[list]) -> Self:
        """Get the Size of a nested list"""
        height = len(lst)
        width = nested_len(lst)

        return Size(height, width)

    def __init__(self, width: int, height: int):
        if height < 0 or width < 0:
            raise NegativeError({"height": height, "width": width}, type(self))

    @property
    def height(self) -> int:
        return self.y

    @property
    def width(self) -> int:
        return self.x

    @property
    def inner(self) -> Self:
        """-2"""
        return self - 2

    @property
    def i(self) -> Self:
        """The indexing size"""
        return self - 1

    def __repr__(self) -> str:
        """Size(height, width)"""
        return f"Size(height={self.height}, width={self.width})"

    def __contains__(self, item: Coord):
        """"""
        return self.height <= item.y and self.width <= item.y
        # return item in rect_range(self)

    @property
    def dis(self) -> float:
        """The distance (the amount of points) between the origin (0, 0)"""
        return sqrt(self.x**2 + self.y**2)

    @property
    def compare_dis(self) -> int:
        """Compare the distance between the origin of Size's"""
        return self.x**2 + self.y**2

    @property
    def area(self) -> int:
        """The amount of points within the Size"""
        return (self.x + 1) * (self.y + 1)

    def __lt__(self, __other) -> bool:
        """Compare area"""
        y, x = type(self)._convert(__other)
        return self.area < (y + 1) * (x + 1)


# class Coord:
#     """Represents a 2D coordinate with positive values only, in the format of (y, x) or (row, col)"""

#     def __mul__(self, other) -> Self:
#         other = type(self)._convert(other)
#         return type(self)(self.y * other.y, self.x * other.x)

#     def __init__(self, y: int, x: int) -> None:
#         self.y = y
#         self.x = x

#     @property
#     def coords(self) -> tuple[int, int]:
#         """Returns the current (y, x) coordinates as a tuple"""
#         return self.y, self.x

#     @property
#     def x(self):
#         return self.__x

#     @x.setter
#     def x(self, to: int):
#         self.__x = max(0, to)

#     @property
#     def y(self):
#         return self.__y

#     @y.setter
#     def y(self, to: int):
#         self.__y = max(0, to)

#     @classmethod
#     def _convert(cls, obj: Self | int) -> Self:
#         """Tries to convert the object to a Coord object

#         Raises InvalidConvertType error on invalid object type"""
#         if isinstance(obj, Coord):
#             return obj
#         elif isinstance(obj, int):
#             return cls(obj, obj)
#         raise InvalidConvertType(type(obj), cls)

#     def __iter__(self):
#         return iter(self.coords)

#     def __add__(self, other) -> Self:
#         other = type(self)._convert(other)
#         return type(self)(self.y + other.y, self.x + other.x)

#     def __sub__(self, other) -> Self:
#         other = type(self)._convert(other)
#         return type(self)(self.y - other.y, self.x - other.x)

#     def __eq__(self, other) -> bool:
#         if isinstance(other, (Coord, int)):
#             other = type(self)._convert(other)
#             return self.coords == other.coords
#         return False

#     def __lt__(self, other) -> bool:
#         # Lexicographical Sorting
#         other = type(self)._convert(other)
#         return self.coords < other.coords

#     def __repr__(self) -> str:
#         return f"Coord(y={self.y}, x={self.x})"

#     def __hash__(self) -> int:
#         return hash(self.coords)

#     def distance(self, other: Self) -> float:
#         """Get the distance between one coord and another"""
#         return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
