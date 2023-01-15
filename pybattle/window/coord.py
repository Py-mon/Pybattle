from typing import Optional, Self, Sequence, overload, Any

from pybattle.types_ import CoordReference, SizeReference


# class Coord:
#     """2D coordinates `(y, x)` `(row, col)`.
    
#     Returns given arg(s) if unable to convert to a Coord."""

#     def __new__(cls, data, *_) -> Any:
#         if not isinstance(data, (int, cls, tuple)):
#             return data
#         return super().__new__(cls)
        
#     @overload
#     def __init__(self, y: int, x: Optional[int], /) -> None: ...

#     @overload
#     def __init__(self, xy: int, /) -> None: ...

#     @overload
#     def __init__(self, coord: Self, /) -> None: ...

#     @overload
#     def __init__(self, tup: tuple[int, int], /) -> None: ...
    
#     @overload
#     def __init__(self, other: Any, /) -> None: ...

#     def __init__(self, y, x=None, /) -> None:
#         if isinstance(y, int):
#             if isinstance(x, int):
#                 y, x = y, x
#             else:
#                 y, x = y, y
#         elif isinstance(y, Coord | tuple):
#             y, x = y
#         else:
#             return

#         self.y: int = y
#         self.x: int = x

#     @property
#     def coords(self) -> tuple[int, int]:
#         return (self.y, self.x)
    
#     @coords.setter
#     def coord(self, to):
#         to = self.__class__(to)
#         self.y = to.y
#         self.x = to.x

#     @property
#     def center(self) -> Self:
#         return self.floor_div(2)

#     def add(self, other: CoordReference | SizeReference) -> Self:
#         other = self.__class__(other)
#         return self.__class__(self.y + other.y, self.x + other.x)

#     def subtract(self, other: CoordReference | SizeReference) -> Self:
#         other = self.__class__(other)
#         return self.__class__(self.y - other.y, self.x - other.x)

#     def floor_div(self, other: CoordReference | SizeReference) -> Self:
#         other = self.__class__(other)
#         return self.__class__(self.y // other.y, self.x // other.x)

#     def __add__(self, other: CoordReference | SizeReference) -> Self:
#         return self.add(other)

#     def __iadd__(self, other: CoordReference | SizeReference) -> Self:
#         return self.add(other)

#     def __sub__(self, other: CoordReference | SizeReference) -> Self:
#         return self.subtract(other)

#     def __isub__(self, other: CoordReference | SizeReference) -> Self:
#         return self.subtract(other)

#     def __iter__(self):
#         return iter(self.coords)

#     def __eq__(self, other: CoordReference | SizeReference) -> bool:
#         other = self.__class__(other)
#         return self.coords == other.coords
    
#     def __lt__(self, other: CoordReference | SizeReference) -> bool:
#         other = self.__class__(other)
#         return self.coords < other.coords
    
#     def __contains__(self, sequence: Sequence[CoordReference | SizeReference]) -> bool:
#         for coord in sequence:
#             coord = self.__class__(coord)
#             if self.x == coord.x and self.y == coord.y:
#                 return True
#         return False

#     def __repr__(self) -> str:
#         return f'Coord(y={self.y}, x={self.x})'


class Coord:
    """2D coordinates `(y, x)` `(row, col)`."""

    def __new__(cls, data, *_) -> Any:
        if isinstance(data, cls):
            return data
        return super().__new__(cls)
        
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
        if y is self:
            return
        
        if x is None:
            if isinstance(y, (tuple, self.__class__)):
                self.coords = y
            elif isinstance(y, int):
                self.coords = y, y
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
        return self.floor_div(2)

    def add(self, other: CoordReference | SizeReference) -> Self:
        other = self.__class__(other)
        return self.__class__(self.y + other.y, self.x + other.x)

    def subtract(self, other: CoordReference | SizeReference) -> Self:
        other = self.__class__(other)
        return self.__class__(self.y - other.y, self.x - other.x)

    def floor_div(self, other: CoordReference | SizeReference) -> Self:
        other = self.__class__(other)
        return self.__class__(self.y // other.y, self.x // other.x)

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
        other = self.__class__(other)
        return self.coords == other.coords
    
    def __lt__(self, other: CoordReference | SizeReference) -> bool:
        other = self.__class__(other)
        return self.coords < other.coords
    
    def __contains__(self, sequence: Sequence[CoordReference | SizeReference]) -> bool:
        return self.coords in sequence

    def __repr__(self) -> str:
        return f'Coord(y={self.y}, x={self.x})'
