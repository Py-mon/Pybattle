from collections.abc import Iterable
from math import sqrt
from typing import Iterable, NamedTuple, Optional, Self

from pybattle.screen.grid.nested import max_len


class Point(NamedTuple):
    "Immutable 2D point in the format of (y, x) or (row, col)"

    y: int
    x: int
    
    def __class_getitem__(cls, item):
        subs = cls.__subclasses__()
        return subs[subs.index(item)]

    @property
    def reversed(self):
        return type(self)(self.x, self.y)

    @classmethod
    def _convert(cls, obj: Iterable[int] | Self | int) -> Iterable[int] | Self:
        if not isinstance(obj, int):
            return obj
        return obj, obj

    def __abs__(self) -> Self:
        return type(self)(abs(self.y), abs(self.x))

    @property
    def non_negative(self) -> Self:
        return type(self)(max(self.y, 0), max(self.x, 0))

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

    def __lt__(self, __other) -> bool:
        y, x = type(self)._convert(__other)
        return (self.x + 1) * (self.y + 1) < (y + 1) * (x + 1)

    def distance(self, _other) -> float:
        return sqrt((_other.x - self.x) ** 2 + (_other.y - self.y) ** 2)

    def add_x(self, x):
        return type(self)(self.y, self.x + x)

    def add_y(self, y):
        return type(self)(self.y + y, self.x)
    
    @property
    def neighbors(self) -> tuple[Self, Self, Self, Self]:
        return self.add_x(1), self.add_x(-1), self.add_y(1), self.add_y(1)


class Coord(Point):
    "Immutable 2D coordinate with positive values only, in the format of (y, x) or (row, col)"

    # def __init__(self, y: int, x: int):
    # if y < 0 or x < 0:
    #     raise NegativeError({"y": y, "x": x}, type(self))

    @property
    def coords(self) -> tuple[int, int]:
        """Returns the current (y, x) coordinates as a tuple"""
        return tuple(self)

    @property
    def yx(self) -> tuple[int, int]:
        """Returns the current (y, x) coordinates as a tuple"""
        return tuple(self)

    @property
    def size(self):
        return Size(self.y, self.x)
    
    


class Size(Point):
    """Immutable (height, width) with positive values only, representing the ending coordinate of an object"""

    def __init__(self, height: int, width: int):
        pass

    def rect_range(self, start_from: Optional[Coord] = None) -> list[Coord]:
        """Get a list of coordinates starting at `start` and ending at the Size in a rectangle"""
        start_from = start_from or Coord(0, 0)
        return [
            Coord(y, x)
            for y in range(start_from.y, self.y + 1)
            for x in range(start_from.x, self.x + 1)
        ]

    def array_rect_range(self, start_from: Optional[Coord] = None) -> list[list[Coord]]:
        """Get a nested list of coordinates starting at `start` and ending at the Size in a rectangle"""
        start_from = start_from or Coord(0, 0)
        return [
            [Coord(y, x) for x in range(start_from.x, self.x + 1)]
            for y in range(start_from.y, self.y + 1)
        ]

    def selection_range(
        self, width: int, start_from: Optional[Coord] = None
    ) -> list[Coord]:
        """Get a list of coordinates starting at `start` and ending at the Size (Lexicographical)"""
        start_from = start_from or Coord(0, 0)
        res = [
            Coord(y, x) for y in range(start_from.y, self.y + 1) for x in range(width)
        ]
        res = res[start_from.x : -(width - (self.x + 1))]
        return res

    @property
    def center(self) -> Self:
        """The center point of the Size"""
        return self // 2

    @property
    def coord(self) -> Coord:
        """The size in coordinate form (the ending coordinate)"""
        return Coord(self.y, self.x)

    @classmethod
    def from_str(cls, string: str) -> Self:
        """Get the Size of a str"""
        return Size(string.removeprefix("\n").count("\n"), max_len(string.splitlines()))

    @classmethod
    def from_iter(cls, lst: tuple[tuple, ...]) -> Self:
        """Get the Size of a nested list"""
        height = len(lst)
        width = max_len(lst)

        return Size(height, width)

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
        """The indexing size (-1)"""
        if not hasattr(self, "_i"):
            self._i = self - 1
        return self._i

    def __repr__(self) -> str:
        """Size(height, width)"""
        return f"Size(height={self.height}, width={self.width})"

    def __contains__(self, item: Point):
        """If the coordinate is within the rect range from the origin (0, 0)"""
        return (
            self.height >= item.y
            and self.width >= item.y
            and (self.height != item.y and self.width != item.x)
        )

    def within(self, item: Point, start: Self):
        return item in self and item not in start

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
        """The amount of points within the Size (the length of the rect_range from the origin (0, 0))"""
        return (self.x + 1) * (self.y + 1)



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
