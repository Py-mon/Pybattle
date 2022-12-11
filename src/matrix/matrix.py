from typing import Any, Callable, Generator, Iterator, List, Optional, Self

from src.types_ import CoordReference
from src.window.color import Color, Colors
from src.window.coord import Coord
from src.window.size import Size


class Code:
    """A Color assigned to a coordinate."""

    def __init__(self, coord: CoordReference, color: Color) -> None:
        self.coord = Coord.convert_reference(coord)
        self.color = color

    def __iter__(self) -> Iterator[Coord | Color]:
        return iter((self.coord, self.color))
    

class Range:
    def __init__(
        self, stop: CoordReference | int,
        start: Optional[CoordReference] | int = None
    ) -> None:
        self.start = Coord.convert_reference(start)
        self.stop = Coord.convert_reference(stop)

    @property
    def x_slice(self) -> slice:
        return slice(self.start.x, self.stop.x)
    
    @property
    def y_slice(self) -> slice:
        return slice(self.start.y, self.stop.y)

    @property
    def coords(self) -> List[Coord]:
        return [Coord(self.start.y + col, self.start.x + row) for col in range(self.stop.x + 1) for row in range(self.stop.y + 1)]


class Matrix:
    @staticmethod
    def with_colors(func: Callable[["Matrix"], Any]) -> Callable[["Matrix"], Any]:
        """Includes colors."""

        def wrapper(self: Self, *args) -> Any:
            for (coord, code) in self.colors:
                self.insert(coord, code)
            res = func(self, *args)
            for i, (coord, _) in enumerate(self.colors):
                self.remove((coord.x - i, coord.y))
            return res
        return wrapper

    def __init__(self, data: str | List[List], *colors: Code) -> None:
        self.colors = colors

        if isinstance(data, str):
            if data[0] == '\n':
                data = data[1:]
            self.array = [[cell for cell in row] for row in data.splitlines()]
        else:
            self.array = data

        width = max([len(row) for row in self.rows])
        self.array = [row + [" "] * (width - len(row)) for row in self.rows]

    def __iter__(self) -> Iterator[Generator[str, Any, Any]]:
        """Iterate through every cell."""
        for row in self.rows:
            for cell in row:
                yield cell

    def __contains__(self, coord_or_cell: CoordReference | Any) -> bool:
        """Check if a coord or cell is in the Matrix."""
        coord_or_cell = Coord.convert_reference(coord_or_cell)
        if isinstance(coord_or_cell, Coord):
            return coord_or_cell in Range((0, 0), self.width).coords
        else:
            return coord_or_cell in iter(self)

    @property
    def rows(self) -> List[List]:
        return self.array

    @property
    def cols(self) -> List[List]:
        return [list(col) for col in list(zip(*self.rows))]

    @property
    def size(self) -> Size:
        return Size(self.height, self.width)

    @property
    def width(self) -> int:
        """The max width."""
        return max([len(row) for row in self.rows])

    @property
    def height(self) -> int:
        return max([len(col) for col in self.cols])

    def insert(self, pos: CoordReference, cell: str | Color):
        pos = Coord.convert_reference(pos)
        self.array[pos.y].insert(pos.x, cell)

    def remove(self, pos: CoordReference):
        pos = Coord.convert_reference(pos)
        self.array[pos.y].pop(pos.x)

    def __getitem__(self, coord: CoordReference) -> Any:
        coord = Coord.convert_reference(coord)
        return self.array[coord.y][coord.x]

    def __setitem__(self, coord: CoordReference, cell: Any) -> Any:
        coord = Coord.convert_reference(coord)
        self.array[coord.y][coord.x] = cell

    @with_colors
    def __repr__(self) -> str:
        color = str(Colors.DEFAULT)
        res = '['
        for row in self.array:
            row_ = '['
            for cell in row:
                if isinstance(cell, Color):
                    color = cell._color_code
                    row_ += color
                else:
                    row_ += color + cell + str(Colors.DEFAULT) + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + str(Colors.DEFAULT) + ']'
        return res

    @with_colors
    def __str__(self) -> str:
        return "".join([str(char) for row in self.array for char in row + ['\n']])[:-1] + str(Colors.DEFAULT)
