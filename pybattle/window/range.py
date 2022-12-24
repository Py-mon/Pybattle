from typing import Optional, Generator

from pybattle.types_ import CoordReference
from pybattle.window.coord import Coord


class Range:
    def __init__(
        self, stop: CoordReference,
        start: Optional[CoordReference] = None
    ) -> None:
        self.__start = Coord(start or 0)
        self.__stop = Coord(stop)
        
        if self.__start.y == self.__stop.y:
            self.__stop.y += 1
        if self.__start.x == self.__stop.x:
            self.__stop.x += 1
        
    def __iter__(self) -> Generator[Coord, None, None]:
        for row in self.rows_coords:
            for coord in row:
                yield coord
                
    def __contains__(self, coord: CoordReference) -> bool:
        return Coord(coord) in iter(self)

    @property
    def rows_coords(self) -> list[list[Coord]]:
        return [[
            Coord(y, x) for x in range(self.__start.x, self.__stop.x)]
            for y in range(self.__start.y, self.__stop.y)]  # Strange + 1
