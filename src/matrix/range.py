from typing import List, Optional, Generator

from src.types_ import CoordReference
from src.window.coord import Coord


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

    @property
    def x_slice(self) -> slice:
        return slice(self.start.x, self.stop.x)

    @property
    def y_slice(self) -> slice:
        return slice(self.start.y, self.stop.y)

    @property
    def row_coords(self) -> List[List[Coord]]:
        return [[
            Coord(self.start.y + col, self.start.x + row)
            for col in range(self.stop.x + 1)]
            for row in range(self.stop.y + 1)]
