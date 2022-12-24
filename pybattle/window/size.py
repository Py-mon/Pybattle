from pybattle.window.coord import Coord
from pybattle.window.range import Range
from typing import overload, Self, Any


class Size(Coord, Range):
    @overload
    def __init__(self, height: int, width: int, /) -> None: ...
    
    @overload
    def __init__(self, hw: int, /) -> None: ...
    
    @overload
    def __init__(self, size: Self, /) -> None: ...
    
    @overload
    def __init__(self, tup: tuple[int, int], /) -> None: ...
    
    @overload
    def __init__(self, other: Any, /) -> None: ...
    
    def __init__(self, height, width = None, /) -> None:
        Coord.__init__(self, height, width)
        Range.__init__(self, self.coords)

    @property
    def height(self) -> int:
        return self.y

    @property
    def width(self) -> int:
        return self.x
    
    @property
    def inner_height(self) -> int:
        return self.height - 2
    
    @property
    def inner_width(self) -> int:
        return self.width - 2

    def __repr__(self) -> str:
        return f'Size(height={self.height}, width={self.width})'
