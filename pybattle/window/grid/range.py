from typing import Optional, Generator, Self

from pybattle.window.grid.coord import Coord
from math import ceil


class RectRange:
    def __init__(self, stop: Coord, start: Optional[Coord] = None) -> None:
        if start:
            self.start = start
        else:
            self.start = Coord(0, 0)

        self.stop = stop

    def __iter__(self) -> Generator[Coord, None, None]:
        lst = [coord for row in self.array_coords for coord in row]
        yield from lst

    def __contains__(self, coord: Coord) -> bool:
        return coord in iter(self)

    @property
    def array_coords(self) -> list[list[Coord]]:
        return [
            [Coord(y, x) for x in range(self.start.x, self.stop.x + 1)]
            for y in range(self.start.y, self.stop.y + 1)
        ]

    def __repr__(self) -> str:
        return f"{self.start}: {self.stop}"

    def __add__(self, coord: Coord):
        return RectRange(self.stop + coord, self.start + coord)

    @classmethod
    def center_range(cls, outer_size: Coord, inner_size: Coord) -> Self:
        return cls(
            Coord(
                ceil((outer_size.y + inner_size.y) / 2 - 1),
                ceil((outer_size.x + inner_size.x) / 2 - 1),
            ),
            Coord(
                ceil((outer_size.y - inner_size.y) / 2 - 1),
                ceil((outer_size.x - inner_size.x) / 2 - 1),
            ),
        )



class SelectionRange(RectRange):
    def __init__(
        self,
        width: int,
        stop: Coord,
        start: Optional[Coord] = None,
    ) -> None:
        super().__init__(stop, start)
        self.width = width

    @property
    def array_coords(self) -> list[list[Coord]]:
        res = [
            [Coord(y, x) for x in range(self.width)]
            for y in range(self.start.y, self.stop.y + 1)
        ]
        res[0] = res[0][self.start.x :]
        res[-1] = res[-1][: self.stop.x + 1]
        return res
