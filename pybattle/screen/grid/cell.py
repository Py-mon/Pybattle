from collections.abc import Iterable
from typing import Any, Literal, Self

from pybattle.screen.colors import Color, Colors

# from pybattle.screen.grid.point import Size


# class Container:
#     def __init__(self, cell):
#         self.cell = cell

#     def __repr__(self):
#         return repr(self.cell)


class Cell:
    """A Cell in a matrix."""

    def __init__(
        self,
        value: Any,
        color: Color = Colors.DEFAULT,
        collision: bool = ...,
    ) -> None:
        self._value = value

        self.collision = collision
        if self.collision is ...:
            self.collision = True
            if self._value == " ":
                self.collision = False

        self.color = color

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self) -> str:
        return str(self._value)

    def __len__(self) -> Literal[0]:
        return 0

    @classmethod
    def from_iter(cls, itr: Iterable) -> tuple[Self, ...]:
        """Create a list of cells from an iterable."""
        return tuple(Cell(cell) for cell in itr)

    @classmethod
    def from_str(cls, string: str) -> tuple[tuple[Self, ...], ...]:
        return tuple(
            cls.from_iter(row) for row in string.removeprefix("\n").splitlines()
        )

    @classmethod
    def from_size(cls, size, fill_with: str = " "):
        return tuple(
            tuple(cls(fill_with) for _ in range(size.width)) for _ in range(size.height)
        )

    def __mul__(self, times: int) -> tuple[Self, ...]:
        return tuple(Cell(self._value, self.color) for _ in range(times))

    def __eq__(self, to):
        return self._value == to._value  # add colors

    def __hash__(self) -> int:
        return hash((self.value, self.color))  # add colors
