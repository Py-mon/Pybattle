from typing import Any, Callable, Generator, Iterator, List, Self, Tuple, overload

from pybattle.ansi.colors import Color, Colors
from pybattle.errors import OutOfBoundsError
from pybattle.log import Logger
from pybattle.types_ import CoordReference, SizeReference
from pybattle.window.coord import Coord
from pybattle.window.range import Range
from pybattle.window.size import Size


class ColorCoord:
    """A Color assigned to a coordinate."""

    def __init__(self, coord: CoordReference, color: Color) -> None:
        self.coord = Coord(coord)
        self.color = color

    def __iter__(self) -> Iterator[Coord | Color]:
        return iter((self.coord, self.color))


class Matrix:  
    def __new__(cls, data, *_):
        if isinstance(data, cls):
            return data
        return super().__new__(cls)
    
    @overload
    def __init__(self, size: SizeReference, /, *colors: ColorCoord) -> None: ...
    
    @overload
    def __init__(self, string: str, /, *colors: ColorCoord) -> None: ...
    
    @overload
    def __init__(self, nested_list:  list[Any] | list[list[Any]], /, *colors: ColorCoord) -> None: ...

    @overload
    def __init__(self, matrix: Self, /, *colors: ColorCoord) -> None: ...

    def __init__(self, data, /, *colors: ColorCoord) -> None:
        if data is self:
            return

        self.colors = list(colors)

        if isinstance(Size(data), Size):
            data = Size(data)
            self.array = [[' ' for _ in range(data.width)]
                          for _ in range(data.height)]
            
        elif isinstance(data, str):
            if data[0] == '\n':
                data = data[1:]
            self.array = [[cell for cell in row] for row in data.splitlines()]
            
        elif isinstance(data, list):
            self.array = [list(row) if hasattr(row, '__iter__') else [row] for row in data]

        if self.rows:
            width = max([len(row) for row in self.rows])
            self.array = [row + [" "] * (width - len(row)) for row in self.rows]

        for color in self.colors:
            if color.coord.x >= self.width:
                Logger.warning(
                    f'Coord x: {color.coord.x} is passed the bounds of {self.width}. This may cause unintended problems.')

    @property
    def coords(self) -> list[Coord]:
        return list(iter(Range(self.size)))

    @property
    def rows_coords(self) -> list[list[Coord]]:
        return Range(self.size).rows_coords

    def __contains__(self, coord_or_cell: CoordReference | Any) -> bool:
        """Check if a coord or cell is in the Matrix."""
        coord_or_cell = Coord(coord_or_cell)
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
                return
            return res
        return wrapper
    
    @overload
    def __getitem__(self, row: int) -> Self: ...
    
    @overload
    def __getitem__(self, slice_: slice) -> Self: ...

    @overload
    def __getitem__(self, coord: CoordReference) -> Any: ...
    
    @log_out_of_bounds
    def __getitem__(self, slice_):
        """
        ```
        matrix[n] -> Row n
        matrix[x, y] -> Cell at (x, y) # Note: array[(x, y)] == array[x, y]
        matrix[(sx, sy):(ex, ey)] -> Matrix from (sx, sy) to (ex, ey)
        """
        if isinstance(slice_, int):
            return Matrix(self.array[slice_])

        elif isinstance(slice_, Size | Coord | tuple):
            coord = Coord(slice_)
            return self.array[coord.y][coord.x]

        elif isinstance(slice_, slice):
            stop = Size(slice_.stop)
            if stop is None:
                stop = Size(self.width, self.height) - slice_.start

            return Matrix([[self[coord] for coord in row] for row in Range(stop, slice_.start).rows_coords])
    
    @overload
    def __setitem__(self, row: int, new_row: list[Any]) -> None: ...

    @overload
    def __setitem__(self, coord: CoordReference | SizeReference, cell: Any) -> None: ...
    
    @overload
    def __setitem__(self, slice_: slice, matrix: Self) -> Self: ...
    
    @log_out_of_bounds
    def __setitem__(self, slice_, cell_s) -> None:
        """
        ```
        matrix[n] -> Row n
        matrix[x, y] -> Cell at (x, y) # Note: array[(x, y)] == array[x, y]
        matrix[(sx, sy):(ex, ey)] -> Matrix from (sx, sy) to (ex, ey)
        """
        # TODO: Remove and add colors in area

        if isinstance(slice_, int):
            self.array[slice_] = cell_s

        elif isinstance(slice_, Size | Coord | tuple):
            coord = Coord(slice_)
            self.array[coord.y][coord.x] = cell_s

        elif isinstance(slice_, slice):
            stop = Size(slice_.stop)
            if stop is None:
                stop = Size(self.width, self.height) - slice_.start

            for coord in Range(stop, slice_.start):
                self[coord] = cell_s[coord - slice_.start]

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
        pos = Coord(pos)
        self.array[pos.y].insert(pos.x, cell)

    def pop(self, pos: CoordReference) -> None:
        """Remove the cell at a given pos."""
        pos = Coord(pos)
        self.array[pos.y].pop(pos.x)

    def remove(self, cell: Any) -> None:
        """Remove the first occurrence of a cell."""
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
                self.insert((coord.y, coord.x + i), code)

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
                    row_ += color + str(cell) + str(Colors.DEFAULT) + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + str(Colors.DEFAULT) + ']'
        return res

    @with_colors
    def __str__(self) -> str:
        return "".join([str(char) for row in self.array for char in row + ['\n']])[:-1] + str(Colors.DEFAULT)
    
