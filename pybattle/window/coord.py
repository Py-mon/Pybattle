from pybattle.types_ import CoordReference, SizeReference
from typing import Any, Sequence, Self, Tuple


class Coord:
    """2D coordinates `(y, x)` `(row, col)`."""

    def __init__(
        self,
        y: int = 0,
        x: int = 0,
    ) -> None:
        self.__y = y
        self.__x = x
        
    @property
    def y(self) -> int:
        return self.__y
    
    @y.setter
    def y(self, y: int) -> None:
        self.__y = y
    
    @property
    def x(self) -> int:
        return self.__x
    
    @x.setter
    def x(self, x: int) -> None:
        self.__x = x
    
    @classmethod
    def convert_reference(cls, reference: CoordReference | SizeReference | Any) -> Self:
        """
        ```
        Coord(5, 5) -> Coord(5, 5)
        (1, 3) -> Coord(1, 3)
        Size(2, 4) -> Coord(2, 4)
        """
        if isinstance(reference, int):
            return cls(reference, reference)
        if isinstance(reference, (Coord, Tuple, *Coord.__subclasses__())):
            return cls(*reference)
        return reference

    @property
    def coords(self) -> Tuple[int, int]:
        return (self.__y, self.__x)

    @property
    def center(self) -> Self:
        return self.floor_div(2)

    def add(self, other: CoordReference | SizeReference) -> Self:
        other = self.__class__.convert_reference(other)
        return self.__class__(self.__y + other.__y, self.__x + other.__x)

    def subtract(self, other: CoordReference | SizeReference) -> Self:
        other = self.__class__.convert_reference(other)
        return self.__class__(self.__y - other.__y, self.__x - other.__x)
    
    def floor_div(self, other: CoordReference | SizeReference) -> Self:
        other = self.__class__.convert_reference(other)
        return self.__class__(self.__y // other.__y, self.__x // other.__x)

    def __add__(self, other: CoordReference | SizeReference) -> Self:
        return self.add(other)
    def __iadd__(self, other: CoordReference | SizeReference) -> Self:
        return self.add(other)

    def __sub__(self, other: CoordReference | SizeReference) -> Self:
        return self.subtract(other)
    def __isub__(self, other: CoordReference | SizeReference) -> Self:
        return self.subtract(other)

    def __iter__(self):
        return iter(self.coords)

    def __eq__(self, other: CoordReference | SizeReference) -> bool:
        other = self.__class__.convert_reference(other)
        if self.__x == other.x and self.__y == other.y:
            return True
        return False

    def __contains__(self, sequence: Sequence[CoordReference | SizeReference]) -> bool:
        for coord in sequence:
            coord = self.__class__.convert_reference(coord)
            if self.__x == coord.__x and self.__y == coord.__y:
                return True
        return False

    def __repr__(self) -> str:
        return f'Coord(y={self.__y}, x={self.__x})'
 