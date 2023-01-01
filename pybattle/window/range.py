from typing import Optional, Generator

from pybattle.types_ import CoordReference
from pybattle.window.coord import Coord


class RectRange:
    def __init__(
        self, 
        stop: CoordReference,
        start: Optional[CoordReference] = None
    ) -> None:
        self._start = Coord(start or 0)
        self._stop = Coord(stop)

    def __iter__(self) -> Generator[Coord, None, None]:
        lst = [coord for row in self.array_coords for coord in row]
        yield from lst

    def __contains__(self, coord: CoordReference) -> bool:
        return Coord(coord) in iter(self)

    @property
    def array_coords(self) -> list[list[Coord]]:
        return [[
            Coord(y, x) for x in range(self._start.x, self._stop.x + 1)]
            for y in range(self._start.y, self._stop.y + 1)]
    
    def __repr__(self) -> str:
        return str(self.array_coords)



class SelectionRange(RectRange):
    def __init__(
        self, 
        width: int,
        stop: CoordReference,
        start: Optional[CoordReference] = None,        
    ) -> None:
        super().__init__(stop, start)
        self.width = width
        
    @property
    def array_coords(self) -> list[Coord]:
        res = [[
            Coord(y, x) for x in range(self.width)]
            for y in range(self._start.y, self._stop.y + 1)]
        res[0] = res[0][self._start.x:]
        res[-1] = res[-1][:self._stop.x + 1]
        return res
