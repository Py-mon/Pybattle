from pybattle.types_ import CoordReference
from typing import Any, Sequence, Self, Tuple
from pybattle.log import Logger
from pybattle.error import InvalidMethodError


class Coord:
    """2D coordinates `(y, x)` `(row, col)`."""

    def __init__(
        self,
        y: int = 0,
        x: int = 0,
    ) -> None:
        self._y = y
        self._x = x
        
    @property
    def y(self) -> int:
        return self._y
    
    @property
    def x(self) -> int:
        return self._x

    @classmethod
    def convert_reference(cls, reference: CoordReference | Any) -> "Coord":
        """
        ```
        Coord(5, 5) -> Coord(5, 5)
        (1, 3) -> Coord(1, 3)
        Size(2, 4) -> Coord(2, 4)
        """
        if isinstance(reference, int):
            return cls(reference, reference)
        if isinstance(reference, (Coord, Tuple, *tuple(Coord.__subclasses__()))):
            return cls(*reference)
        return cls(reference)

    @property
    def coords(self) -> Tuple[int, int]:
        """(x, y)"""
        return (self._y, self._x)

    @property
    def center(self) -> Self:
        return self.floor_div(2)

    def add(self, other: CoordReference) -> Self:
        other = Coord.convert_reference(other)
        return Coord(self._y + other._y, self._x + other._x)

    def subtract(self, other: CoordReference) -> Self:
        other = Coord.convert_reference(other)
        return Coord(self._y - other._y, self._x - other._x)
    
    def floor_div(self, other: CoordReference) -> Self:
        other = Coord.convert_reference(other)
        return Coord(self._y // other._y, self._x // other._x)

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
        if self._x == other.x and self._y == other.y:
            return True
        return False

    def __contains__(self, sequence: Sequence[CoordReference]) -> bool:
        for coord in sequence:
            coord = Coord.convert_reference(coord)
            if self._x == coord._x and self._y == coord._y:
                return True
        return False

    def __repr__(self) -> str:
        return f'Coord(y={self._y}, x={self._x})'
    
    
class Size(Coord):
    def __repr__(self) -> str:
        return f'Size(height={self._x}, width={self._y})'
    
    @property
    def height(self):
        return self._y
    
    @property
    def width(self):
        return self._x
    
    @property
    def y(self):
        Logger.error(error=InvalidMethodError)
    
    @property
    def x(self):
        Logger.error(error=InvalidMethodError)