from typing import Self
from source.types_ import CoordReference


class Coord:
    """2D coordinates (x, y) (col, row)."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0
        
    ) -> None:
        self.y = y
        self.x = x
        
    @staticmethod
    def convert_reference(reference: CoordReference) -> "Coord":
        if isinstance(reference, tuple):
            return Coord(*reference)
        return reference
        
    @property
    def reverse(self) -> tuple[int, int]:
        """(y, x)"""
        return (self.y, self.x)

    @property
    def coords(self) -> tuple[int, int]:
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

    def __contains__(self, sequence: CoordReference) -> bool:
        for coord in sequence:
            coord = Coord.convert_reference(coord)
            if self.x == coord.x and self.y == coord.y:
                return True
        return False

    def __repr__(self) -> str:
        return f'(x: {self.x}, y: {self.y})'


class CoordList:
    def __init__(self, start: CoordReference, end: CoordReference) -> None:
        self.start = Coord.convert_reference(start)
        self.end = Coord.convert_reference(end)

    def get_range(self) -> list[Self]:
        return [Coord(self.start.x + col, self.start.y + row) for col in range(self.end.x + 1) for row in range(self.end.y + 1)]
