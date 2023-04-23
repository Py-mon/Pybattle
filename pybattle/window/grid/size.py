from typing import Self, Iterable

from pybattle.window.grid.coord import Coord
from pybattle.window.grid.range import RectRange
from pybattle.log.errors import InvalidConvertType
from pybattle.types_ import is_nested, nested_len


class Size(Coord, RectRange):
    @classmethod
    def from_str(cls, string: str) -> Self:
        """Create a Size from a str."""
        while string.startswith("\n"):
            string = string[1:]

        return Size(string.count("\n"), nested_len(string.splitlines()))

    @classmethod
    def from_list(cls, lst: list) -> Self:
        """Create a Size from a list."""
        height = len(lst)
        width = nested_len(lst)

        if not is_nested(lst):
            height = 0

        return Size(height, width)

    @classmethod
    def from_iter(cls, iter_: Iterable) -> Self:
        """Create a Size from a iterable."""
        return Size(*iter_)

    @classmethod
    def _convert(cls, obj) -> Self:
        if isinstance(obj, list):
            obj = cls.from_list(obj)
        if hasattr(obj, "__iter__"):
            obj = cls.from_iter(obj)
        elif isinstance(obj, str):
            obj = cls.from_str(obj)
        elif isinstance(obj, int):
            obj = cls(obj, obj)
        else:
            raise InvalidConvertType(type(obj), cls)
        return obj

    def __init__(self, height: int, width: int) -> None:
        Coord.__init__(self, height, width)
        RectRange.__init__(self, self)

    @property
    def height(self) -> int:
        return self.y

    @property
    def width(self) -> int:
        return self.x

    @property
    def inner(self) -> Self:
        """The inner part from along the edge excluding the corners

        ```
          vvv
        ╭ ─── ╮
          ^^^
         ```
        """
        return self - 2

    @property
    def i(self) -> Self:
        """The true size (0 inclusive)

        ```
        0 1 2 3 4
        ╭ ─ ─ ─ ╮
         ```
        """
        return self - 1

    def __repr__(self) -> str:
        """Size(height, width)"""
        return f"Size(height={self.height}, width={self.width})"
