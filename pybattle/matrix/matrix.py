from typing import Any, Callable, Generator, Iterator, List, Self, Tuple

from pybattle.error import OutOfBoundsError
from pybattle.log import Logger
from pybattle.matrix.range import Range
from pybattle.types_ import CoordReference
from pybattle.window.color import Color, Colors
from pybattle.window.coord import Coord
from pybattle.window.size import Size


class ColorCoord:
    """A Color assigned to a coordinate."""

    def __init__(self, coord: CoordReference, color: Color) -> None:
        self.coord = Coord.convert_reference(coord)
        self.color = color

    def __iter__(self) -> Iterator[Coord | Color]:
        return iter((self.coord, self.color))


class Matrix:
    def __init__(self, data: str | List[List] | List, *colors: ColorCoord) -> None:
        self.colors = colors

        if isinstance(data, str):
            if data[0] == '\n':
                data = data[1:]
            self.array = [[cell for cell in row] for row in data.splitlines()]
        else:
            self.array = data
            if not all([isinstance(row, list) for row in self.array]):
                self.array = [self.array]

        width = max([len(row) for row in self.rows])
        self.array = [row + [" "] * (width - len(row)) for row in self.rows]

        for color in self.colors:
            if color.coord.x >= self.width:
                Logger.warning(
                    f'Coord x: {color.coord.x} is passed the bounds of {self.width}. This may cause unintended problems.')
            for color_ in self.colors:
                # TODO if color.coord.x == color_.coord.x: not == but around by 1
                ...

    @property
    def coords(self) -> List[Coord]:
        return list(iter(Range(self.size.reverse)))

    @property
    def row_coords(self, row: int) -> List[Coord]:
        return Range((len(row), row), (0, row))

    def __contains__(self, coord_or_cell: CoordReference | Any) -> bool:
        """Check if a coord or cell is in the Matrix."""
        coord_or_cell = Coord.convert_reference(coord_or_cell)
        if isinstance(coord_or_cell, Coord):
            return coord_or_cell in self.coords
        else:
            return coord_or_cell in iter(self)

    def __iter__(self) -> Generator[Any, None, None]:
        """Iterate through every cell."""
        for row in self.rows:
            for cell in row:
                yield cell

    @staticmethod
    def log_out_of_bounds(func: Callable) -> Callable:
        """Logs on IndexError."""

        def wrapper(self: Self, *args) -> Any:
            try:
                res = func(self, *args)
            except IndexError:
                Logger.error('Index out of range.', OutOfBoundsError)
            return res
        return wrapper

    @log_out_of_bounds
    def __getitem__(
        self,
        slice_: int | tuple[int, int] | Tuple[CoordReference,
                                              CoordReference] | slice
    ) -> Self | Any:
        """
        ```
        matrix[n] -> Row n
        matrix[x, y] -> Cell at (x, y) # Note: array[(x, y)] == array[x, y]
        matrix[(sx, sy):(ex, ey)] -> Matrix from (sx, sy) to (ex, ey)
        """
        if isinstance(slice_, int):
            return Matrix(self.array[slice_])

        elif isinstance(slice_, Coord | tuple):
            coord = Coord.convert_reference(slice_)
            return self.array[coord.y][coord.x]

        elif isinstance(slice_, slice):
            stop = slice_.stop
            if stop is None:
                stop = (self.width - 1, self.height - 1)

            return Matrix([[self[coord] for coord in row] for row in Range(slice_.stop, slice_.start).row_coords])

    @log_out_of_bounds
    def __setitem__(
        self,
        slice_: int | Tuple[int, int] | Tuple[CoordReference,
                                              CoordReference] | slice,
        cell_s: Any | List | Self | List[List]
    ) -> None:
        """
        ```
        matrix[n] -> Row n
        matrix[x, y] -> Cell at (x, y) # Note: array[(x, y)] == array[x, y]
        matrix[(sx, sy):(ex, ey)] -> Matrix from (sx, sy) to (ex, ey)
        """
        # TODO: Remove colors in area
        
        if isinstance(slice_, int):
            self.array[slice_] = cell_s

        elif isinstance(slice_, Coord | tuple):
            coord = Coord.convert_reference(slice_)
            self.array[coord.y][coord.x] = cell_s

        elif isinstance(slice_, slice):
            stop = slice_.stop
            if stop is None:
                stop = (self.width - 1, self.height - 1)
            
            for coord in Range(stop + 1, slice_.start):
                self[coord] = cell_s[coord]

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

    def insert(self, pos: CoordReference, cell: Any) -> None:
        """Insert a cell at a given pos."""
        pos = Coord.convert_reference(pos)
        self.array[pos.y].insert(pos.x, cell)

    def pop(self, pos: CoordReference) -> None:
        """Remove the cell at a given pos."""
        pos = Coord.convert_reference(pos)
        self.array[pos.y].pop(pos.x)

    def remove(self, cell: Any) -> None:
        """Remove the first occurrence a cell."""
        for i, row in enumerate(self.rows):
            if cell in row:
                self.array[i].remove(cell)

    def remove_colors(self) -> None:
        self.colors = []

    @staticmethod
    def with_colors(func: Callable[["Matrix"], Any]) -> Callable[["Matrix"], Any]:
        """Includes colors in the given function."""

        def wrapper(self: Self, *args) -> Any:
            for i, (coord, code) in enumerate(self.colors):
                self.insert((coord.x + i, coord.y), code)

            res = func(self, *args)

            for _, code in self.colors:
                self.remove(code)
            return res
        return wrapper

    @with_colors
    def __repr__(self) -> str:
        color = str(Colors.DEFAULT)
        res = '['
        for row in self.array:
            row_ = '['
            for cell in row:
                if isinstance(cell, Color):
                    color = str(cell)
                    row_ += color
                else:
                    row_ += color + cell + str(Colors.DEFAULT) + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + str(Colors.DEFAULT) + ']'
        return res

    @with_colors
    def __str__(self) -> str:
        return "".join([str(char) for row in self.array for char in row + ['\n']])[:-1] + str(Colors.DEFAULT)
