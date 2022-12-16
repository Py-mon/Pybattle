from typing import List, Optional, Generator

from pybattle.types_ import CoordReference
from pybattle.matrix.coord import Coord


class Range:
    def __init__(
        self, stop: CoordReference,
        start: Optional[CoordReference] = None
    ) -> None:
        self.start = Coord.convert_reference(start or 0)
        self.stop = Coord.convert_reference(stop)
        
    def __iter__(self) -> Generator[Coord, None, None]:
        for row in self.row_coords:
            for coord in row:
                yield coord
                
    def __contains__(self, coord: CoordReference) -> bool:
        return Coord.convert_reference(coord) in iter(self)

    @property
    def row_coords(self) -> List[List[Coord]]:
        return [[
            Coord(y, x) for x in range(self.start.x, self.stop.x)]
            for y in range(self.start.y, self.stop.y + 1)]  # Strange + 1
