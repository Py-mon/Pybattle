from collections.abc import Iterable
from random import randint
from typing import Iterable, Self

from pybattle.log.errors import InvalidConvertType
from pybattle.types_ import is_nested, nested_len
from pybattle.window.grid.coord import Coord


class Size(Coord):
    """Inclusive"""

    @property
    def center(self) -> Self:
        """The center of the Size"""
        return type(self)(self.height // 2, self.width // 2)

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

    def __init__(self, height: int, width: int) -> None:
        Coord.__init__(self, height, width)

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

    def random(self):
        """Get a random coordinate within the size."""
        return Coord(randint(0, self.height), randint(0, self.width))
