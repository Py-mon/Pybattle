from typing import Optional, Self, Sequence, overload, Any

from pybattle.types_ import CoordReference


class Coord:
    """2D coordinates `(y, x)` `(row, col)`."""

    @overload
    def __init__(self, y: int, x: Optional[int], /) -> None: ...

    @overload
    def __init__(self, xy: int, /) -> None: ...

    @overload
    def __init__(self, coord: Self, /) -> None: ...

    @overload
    def __init__(self, tup: tuple[int, int], /) -> None: ...
    
    @overload
    def __init__(self, other: Any, /) -> None: ...

    def __init__(self, y, x=None, /) -> None:
        if x is None:
            if isinstance(y, tuple):
                self.coords = y
            elif isinstance(y, int):
                self.coords = y, y
            else:
                raise TypeError(f'Invalid Type: {type(y)}')
        else:
            self.coords = y, x

    @property
    def coords(self) -> tuple[int, int]:
        return (self.y, self.x)
    
    @coords.setter
    def coords(self, to: Self | tuple):
        self.y, self.x = to

    @property
    def center(self) -> Self:
        return type(self)(self.y // 2, self.x // 2)
    
    @classmethod
    def _convert(cls, obj: CoordReference) -> Self:
        if not isinstance(obj, cls):
            obj = cls(obj)
        return obj
    
    def __iter__(self):
        return iter(self.coords)

    def __add__(self, other: CoordReference) -> Self:
        other = type(self)._convert(other)
        return type(self)(self.y + other.y, self.x + other.x)

    def __sub__(self, other: CoordReference) -> Self:
        other = type(self)._convert(other)
        return type(self)(self.y - other.y, self.x - other.x)

    def __eq__(self, other: CoordReference) -> bool:
        other = type(self)._convert(other)
        return self.coords == other.coords
    
    def __lt__(self, other: CoordReference) -> bool:
        """Lexicographically sorted."""
        other = type(self)._convert(other)
        return self.coords < other.coords

    def __repr__(self) -> str:
        return f'Coord(y={self.y}, x={self.x})'
    
    def __hash__(self) -> int:
        return hash(self.coords)
