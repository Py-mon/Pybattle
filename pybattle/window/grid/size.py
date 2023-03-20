from typing import Any, Optional, Self, overload

from pybattle.window.grid.coord import Coord
from pybattle.window.grid.range import RectRange
from math import ceil


class Size(Coord, RectRange):
    @overload
    def __init__(self, height: int, width: int, /) -> None: ...
    
    @overload
    def __init__(self, hw: int, /) -> None: ...
    
    @overload
    def __init__(self, tup: tuple[int, int], /) -> None: ...
    
    @overload
    def __init__(self, array: list[list], /) -> None: ...
    
    @overload
    def __init__(self, coord: Coord, /) -> None: ...
    
    @overload
    def __init__(self, string: str, /) -> None: ...
    
    def __init__(self, data, width: Optional[int] = None, /) -> None:
        if isinstance(data, str):
            height = data.count('\n') + 1
            width = max([len(row) for row in data.splitlines()])
        elif isinstance(data, list):
            height = len(data)
            width = max([len(row) for row in data])
        elif isinstance(data, Coord):
            height, width = data
        else:
            height = data
        
        Coord.__init__(self, height, width)
        RectRange.__init__(self, self)

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
