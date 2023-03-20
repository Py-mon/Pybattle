from copy import copy
from typing import Any, Generator, Optional, Self, overload

from pybattle.ansi.colors import Colors, ColorType
from pybattle.debug.log import Logger
from pybattle.types_ import Align, ColorRange, Junction
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.range import RectRange, SelectionRange
from pybattle.window.grid.size import Size
from pybattle.debug.errors import OutOfBoundsError


class Cell:
    def __new__(cls, value, *_, **__):
        if isinstance(value, Cell):
            return value
        return super().__new__(cls)

    def __init__(self, value: Any, color: ColorType = Colors.DEFAULT, junction: Optional[Junction] = None) -> None:
        if value is self:
            return

        self.value = value
        self.color = color

        self.junction = junction
        if self.junction is None:
            self.junction = {}

    def __repr__(self) -> str:
        return str(self.value)

    def __mul__(self, times: int) -> list[Self]:
        return [Cell(self.value, self.color, self.junction) for _ in range(times)]


def level_out(array: list[list[Cell]], alignment: Align) -> list[list[Cell]]:
    if array:
        row_lengths = [len(row) for row in array]
        max_length = max(row_lengths)
        if not all(length == max_length for length in row_lengths):
            width = max(row_lengths)

            def cut(n): return (n // 2, n - (n // 2))

            match alignment:
                case Align.LEFT:
                    return [row + Cell(' ') * (width - len(row)) for row in array]
                case Align.RIGHT:
                    return [Cell(' ') * (width - len(row)) + row for row in array]
                case Align.CENTER:
                    return [Cell(' ') * cut(width - len(row))[0] + row + Cell(' ') * cut(width - len(row))[1] for row in array]
                case _:
                    raise ValueError()
    return array


class Matrix:
    @overload
    def __init__(self, size: Size, /, *
                 colors: ColorRange, alignment: Align = Align.LEFT) -> None: ...

    @overload
    def __init__(self, string: str, /, *
                 colors: ColorRange, alignment: Align = Align.LEFT) -> None: ...

    @overload
    def __init__(self, list: list[Any], /, *colors: ColorRange,
                 alignment: Align = Align.LEFT) -> None: ...

    @overload
    def __init__(self, nested_list: list[list[Any]], /, *
                 colors: ColorRange, alignment: Align = Align.LEFT) -> None: ...

    def __init__(self, data, /, *colors: ColorRange, alignment: Align = Align.LEFT) -> None:
        def cells(row): return [Cell(value) for value in row]

        if isinstance(data, str):
            if data[0] == '\n':
                data = data[1:]
            self.cells = [cells(row) for row in data.splitlines()]

        elif isinstance(data, list):
            self.cells = [cells(row) if hasattr(
                row, '__iter__') else cells([row]) for row in data]

        elif isinstance(data, (Size, Coord, tuple)):
            self.cells = self.create_empty_array(*data)
        else:
            raise TypeError(f'Invalid Type of {type(data)}: {data}')

        self.alignment = alignment
        self.level_out()

        self.colors: list[ColorRange] = []
        self.add_colors(*colors)

    def level_out(self) -> None:
        if self.rows:
            row_lengths = [len(row) for row in self.rows]
            max_length = max(row_lengths)
            if not all(length == max_length for length in row_lengths):
                width = max(row_lengths)

                def cut(n): return (n // 2, n - (n // 2))

                match self.alignment:
                    case Align.LEFT:
                        self.cells = [
                            row + Cell(' ') * (width - len(row)) for row in self.rows]
                    case Align.RIGHT:
                        self.cells = [
                            Cell(' ') * (width - len(row)) + row for row in self.rows]
                    case Align.CENTER:
                        self.cells = [Cell(' ') * cut(width - len(row))[0] + row + Cell(
                            ' ') * cut(width - len(row))[1] for row in self.rows]

    def create_empty_array(self, height, width):
        return [Cell(' ') * width for _ in range(height)]

    def add_color(self, color: ColorType, range_: RectRange | SelectionRange) -> None:
        self.colors.append((color, range_))
        for coord in range_:
            try:
                self[coord].color = color
            except IndexError:
                Logger.error(f'The color {color.name.lower()} is out of bounds at {coord} for {self.size} by {coord - self.size} (from {range_})', OutOfBoundsError)

    def add_colors(self, *colors: ColorRange) -> None:
        for (color, coord) in colors:
            self.add_color(color, coord)

    @property
    def coords(self) -> list[Coord]:
        return list(iter(RectRange(self.size)))

    @property
    def rows_coords(self) -> list[list[Coord]]:
        return RectRange(self.size).array_coords

    @overload
    def __contains__(self, cell: Any, /) -> bool: ...

    @overload
    def __contains__(self, coord: Any, /) -> bool: ...

    def __contains__(self, item: Coord | Any) -> bool:
        """Check if a coord or cell is in the Matrix."""
        if isinstance(item, Coord):
            return item in self.coords
        else:
            return Cell(item) in self

    def __iter__(self) -> Generator[Cell, None, None]:
        """Iterate through every cell."""
        for row in self.rows:
            for cell in row:
                yield cell

    @overload
    def __getitem__(self, row: int, /) -> Self: ...

    @overload
    def __getitem__(self, slice_: slice, /) -> Self: ...

    @overload
    def __getitem__(self, coord: Coord, /) -> Cell: ...

    @overload
    def __getitem__(self, rect_range: RectRange, /) -> None: ...

    def __getitem__(self, item, /):
        if isinstance(item, Coord):
            try:
                return self.cells[item.y][item.x]
            except IndexError:
                Logger.error(f'{item} is out of bounds for {self.size} by {item - self.size}', OutOfBoundsError)

        elif isinstance(item, RectRange):
            return self[item.start: item.stop]

        elif isinstance(item, slice):
            stop = Size(item.stop)
            if stop is None:
                stop = Size(self.width, self.height) - item.start

            return Matrix([[self[coord] for coord in row] for row in RectRange(stop, item.start).array_coords])

        elif isinstance(item, int):
            return Matrix(self.cells[item])

    @overload
    def __setitem__(self, rect_range: RectRange, matrix: Self, /) -> None: ...

    @overload
    def __setitem__(self, coord: Coord, cell: Cell, /) -> None: ...

    @overload
    def __setitem__(self, slice_: slice, matrix: Self, /) -> None: ...

    def __setitem__(self, item, new_cells, /) -> None:
        if isinstance(item, Coord):
            try:
                self.cells[item.y][item.x] = new_cells
            except IndexError:
                Logger.error(f'{item} is out of bounds for {self.size} by {item - self.size}', OutOfBoundsError)

        elif isinstance(item, RectRange):
            self[item.start: item.stop] = new_cells

        elif isinstance(item, slice):
            stop = Size(item.stop)
            if stop is None:
                stop = Size(self.width, self.height) - item.start

            for coord in RectRange(stop, item.start):
                self[coord].value = new_cells[coord - item.start].value
                self[coord].color = new_cells[coord - item.start].color
                self[coord].junction = new_cells[coord - item.start].junction

    @property
    def rows(self) -> list[list[Cell]]:
        return self.cells

    @property
    def cols(self) -> list[list[Cell]]:
        return [list(col) for col in list(zip(*self.rows))]

    @property
    def size(self) -> Size:
        return Size(self.height, self.width) - 1

    @property
    def width(self) -> int:
        return max([len(row) for row in self.rows])

    @property
    def height(self) -> int:
        return max([len(col) for col in self.cols])

    def insert(self, pos: Coord, cell: Cell) -> None:
        """Insert a cell at the given pos."""
        self.cells[pos.y].insert(pos.x, cell)
        self.level_out()

    def pop(self, pos: Coord) -> None:
        """Remove the cell at the given pos."""
        self.cells[pos.y].pop(pos.x)
        self.level_out()

    def remove(self, cell: Cell) -> None:
        """Remove the first occurrence of a cell."""
        for i, row in enumerate(self.rows):
            if cell in row:
                self.cells[i].remove(cell)
        self.level_out()

    def remove_colors(self) -> None:
        self.colors = []

    def __repr__(self) -> str:
        res = '['
        for row in self.cells:
            row_ = '['
            for cell in row:
                row_ += str(cell.value) + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + ']'
        return res

    @property
    def colored_repr(self) -> str:
        res = '['
        for row in self.cells:
            row_ = '['
            for cell in row:
                row_ += str(cell.color) + cell.value + \
                    str(Colors.DEFAULT) + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + str(Colors.DEFAULT) + ']'
        return res

    def __str__(self) -> str:
        return "".join([str(cell.color) + repr(cell) for row in self.cells for cell in row + [Cell('\n')]])[:-1] + str(Colors.DEFAULT)
