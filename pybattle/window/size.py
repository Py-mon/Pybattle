from pybattle.window.coord import Coord
from pybattle.window.range import RectRange
from typing import overload, Self, Any
from pybattle.types_ import CoordReference


class Size(Coord, RectRange):
    def __new__(cls, data, *_) -> Any:
        if not isinstance(data, (int, cls, tuple, str)):
            return data
        return object.__new__(cls)
    
    @overload
    def __init__(self, height: int, width: int, /) -> None: ...
    
    @overload
    def __init__(self, hw: int, /) -> None: ...
    
    @overload
    def __init__(self, size: Self, /) -> None: ...
    
    @overload
    def __init__(self, tup: tuple[int, int], /) -> None: ...
    
    @overload
    def __init__(self, array: list[list], /) -> None: ...
    
    @overload
    def __init__(self, coord: CoordReference, /) -> None: ...
    
    @overload
    def __init__(self, string: str, /) -> None: ...
    
    @overload
    def __init__(self, other: Any, /) -> None: ...
    
    def __init__(self, data, width = None, /) -> None:
        if isinstance(data, str):
            height = data.count('\n') + 1
            width = max([len(row) for row in data.splitlines()])
        elif isinstance(data, list):
            height = len(data)
            width = max([len(row) for row in data])
        else:
            height = data
            
        Coord.__init__(self, height, width)
        RectRange.__init__(self, self.coords)

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
