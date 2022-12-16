"""2D coordinates (x, y) (col, row)."""

from typing import Any, Self, Sequence, Tuple

from pybattle.types_ import CoordReference, SizeReference


class Coord:
    # TODO: Change the (x, y) to (y, x) Note: This is everywhere not just in the Coord class.
    """2D coordinates (x, y) (col, row)."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0

    ) -> None:
        self.y = y
        self.x = x

    @staticmethod
    def convert_reference(reference: CoordReference | int | Any) -> "Coord":
        """
        ```
        Coord(5, 5) -> Coord(5, 5)
        (1, 3) -> Coord(1, 3)
        Size(2, 4) -> Coord(2, 4)
        """
        if isinstance(reference, int):
            return Coord(reference, reference)
        if isinstance(reference, SizeReference):
            return Coord(*reference)
        return reference

    @property
    def reverse(self) -> Tuple[int, int]:
        """(y, x)"""
        return (self.y, self.x)

    @property
    def coords(self) -> Tuple[int, int]:
        """(x, y)"""
        return (self.x, self.y)

    def add(self, other: CoordReference) -> Self:
        other = Coord.convert_reference(other)
        return Coord(self.x + other.x, self.y + other.y)

    def subtract(self, other: CoordReference) -> Self:
        other = Coord.convert_reference(other)
        return Coord(self.x - other.x, self.y - other.y)

    def __add__(self, other: CoordReference) -> Self:
        return self.add(other)

    def __iadd__(self, other: CoordReference) -> Self:
        return self.add(other)

    def __sub__(self, other: CoordReference) -> Self:
        return self.subtract(other)

    def __isub__(self, other: CoordReference) -> Self:
        return self.subtract(other)

    def __iter__(self):
        return iter(self.coords)

    def __eq__(self, other: CoordReference) -> bool:
        other = Coord.convert_reference(other)
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __contains__(self, sequence: Sequence[CoordReference]) -> bool:
        for coord in sequence:
            coord = Coord.convert_reference(coord)
            if self.x == coord.x and self.y == coord.y:
                return True
        return False

    def __repr__(self) -> str:
        return f'Coord(x={self.x}, y={self.y})'


class CoordList:
    def __init__(self, start: CoordReference, end: CoordReference) -> None:
        self.start = Coord.convert_reference(start)
        self.end = Coord.convert_reference(end)

    def get_range(self) -> list[Coord]:
        """Get a range of coords from `start` to `end`."""
        return [Coord(self.start.x + col, self.start.y + row) for col in range(self.end.x + 1) for row in range(self.end.y + 1)]
