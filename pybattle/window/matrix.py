from operator import itemgetter
from typing import Any, Callable, Generator, Self, overload

from pybattle.ansi.colors import Color
from pybattle.log import Logger
from pybattle.types_ import CoordReference, SizeReference
from pybattle.window.coord import Coord
from pybattle.window.range import RectRange, SelectionRange
from pybattle.window.size import Size


class Cell:
    def __new__(cls, value, *_) -> Self:
        if isinstance(value, cls):
            return value
        return super().__new__(cls)
    
    def __init__(self, value: Any, color: Color = None) -> None:
        if self is value:
            return
        
        if color is None:
            color = Color.DEFAULT
        
        self.value = value
        self.color = color

    def __repr__(self) -> str:
        return str(self.value)
    
    def __mul__(self, times: int) -> list[Self]:
        return [Cell(self.value, self.color) for _ in range(times)]



class Matrix:  
    def __new__(cls, data, *_):
        if isinstance(data, cls):
            return data
        return super().__new__(cls)
    
    @overload
    def __init__(self, size: SizeReference, *colors: tuple[CoordReference, Color]) -> None: ...
    
    @overload
    def __init__(self, string: str, *colors: tuple[CoordReference, Color]) -> None: ...
    
    @overload
    def __init__(self, nested_list: list[Any | Cell] | list[list[Any | Cell]], *colors: tuple[CoordReference, Color]) -> None: ...

    @overload
    def __init__(self, matrix: Self) -> None: ...

    def __init__(self, data, *colors: tuple[CoordReference, Color]) -> None:
        if data is self:
            return
        
        self.colors = list(colors)
        self.colors.sort(key=itemgetter(0))

        if isinstance(data, str):
            if data[0] == '\n':
                data = data[1:]
            self.cells = [[Cell(value) for value in row] for row in data.splitlines()]

        elif isinstance(data, list):
            array = [list(row) if hasattr(row, '__iter__') else [row] for row in data]
            self.cells = [[Cell(value) for value in row] for row in array]
        
        elif isinstance(data, (Size, tuple, Coord)):
            if not isinstance(data, Size):
                size = Size(data)
            else:
                size = data
            self.cells = [[Cell(' ') for _ in range(size.x)] for __ in range(size.y)]

        if self.rows:
            row_lengths = [len(row) for row in self.rows]
            if row_lengths.count(row_lengths[0]) != len(row_lengths):
                width = max(row_lengths)
                self.cells = [row + Cell(" ") * (width - len(row)) for row in self.rows]
            
        self.add_colors(*colors)
            
    def next_color(self, coord: CoordReference) -> None:
        color_coords = [color_coord[0] for color_coord in self.colors]

        if len(color_coords) == 0:
            return self.size

        if coord in color_coords:
            if coord == color_coords[-1]:
                return self.size
            index = color_coords.index(coord) + 1
        else:
            copied_list = color_coords.copy()
            copied_list.append(coord)
            copied_list.sort()
            index = copied_list.index(coord)

        coord = Coord(color_coords[index])
        coord = Coord(coord.y, coord.x - 1)
        return coord

    def add_color(self, coord: CoordReference, color: Color) -> None:
        for coord in SelectionRange(self.width, self.next_color(coord), coord):
            self[coord].color = color
            
    def add_colors(self, *colors: tuple[CoordReference, Color]) -> None:
        for (coord, color) in colors:
            self.add_color(coord, color)
            
    def add_rect_color(self, coord: CoordReference, color: Color) -> None:
        for coord in RectRange(self.next_color(coord), coord):
            self[coord].color = color

    @property
    def coords(self) -> list[Coord]:
        return list(iter(RectRange(self.size)))

    @property
    def rows_coords(self) -> list[list[Coord]]:
        return RectRange(self.size).array_coords

    def __contains__(self, coord_or_cell: CoordReference | Any) -> bool:
        """Check if a coord or cell is in the Matrix."""
        coord_or_cell = Coord(coord_or_cell)
        if isinstance(coord_or_cell, Coord):
            return coord_or_cell in self.coords
        else:
            return coord_or_cell in iter(self)

    def __iter__(self) -> Generator[Cell, None, None]:
        """Iterate through every cell."""
        for row in self.rows:
            for cell in row:
                yield cell
    
    @overload
    def __getitem__(self, row: int) -> Self: ...
    
    @overload
    def __getitem__(self, slice_: slice) -> Self: ...

    @overload
    def __getitem__(self, coord: CoordReference) -> Cell: ...
    
    def __getitem__(self, slice_) -> Cell:
        """
        ```
        matrix[n] -> Row n
        matrix[x, y] -> Cell at (x, y) # Note: array[(x, y)] == array[x, y]
        matrix[(sx, sy):(ex, ey)] -> Matrix from (sx, sy) to (ex, ey)
        """
        if isinstance(slice_, Size | Coord | tuple):
            coord = Coord(slice_)
            return self.cells[coord.y][coord.x]

        elif isinstance(slice_, slice):
            stop = Size(slice_.stop)
            if stop is None:
                stop = Size(self.width, self.height) - slice_.start

            return Matrix([[self[coord] for coord in row] for row in RectRange(stop, slice_.start).array_coords])

        elif isinstance(slice_, int):
            return Matrix(self.cells[slice_])
        
    @overload
    def __setitem__(self, coord: CoordReference | SizeReference, cell: Cell) -> None: ...
    
    @overload
    def __setitem__(self, slice_: slice, matrix: Self) -> Self: ...

    def __setitem__(self, slice_, cell_s: Self | Cell) -> None:
        """
        ```
        matrix[n] -> Row n
        matrix[x, y] -> Cell at (x, y) # Note: array[(x, y)] == array[x, y]
        matrix[(sx, sy):(ex, ey)] -> Matrix from (sx, sy) to (ex, ey)
        """
        if isinstance(slice_, Size | Coord | tuple):
            coord = Coord(slice_)
            self.cells[coord.y][coord.x] = Cell(cell_s)

        elif isinstance(slice_, slice):
            stop = Size(slice_.stop)
            if stop is None:
                stop = Size(self.width, self.height) - slice_.start

            for coord in RectRange(stop, slice_.start):
                self[coord] = cell_s[coord - slice_.start]
                
    @overload
    def change_cell_value(self, coord: CoordReference | SizeReference, value: Any) -> None: ...
    
    @overload
    def change_cell_value(self, slice_: slice, matrix: Self) -> Self: ...
                
    def change_cell_value(self, slice_, value: Any) -> None:
        """
        ```
        matrix[n] -> Row n
        matrix[x, y] -> Cell at (x, y) # Note: array[(x, y)] == array[x, y]
        matrix[(sx, sy):(ex, ey)] -> Matrix from (sx, sy) to (ex, ey)
        """
        if isinstance(slice_, Size | Coord | tuple):
            coord = Coord(slice_)
            self.cells[coord.y][coord.x].value = value

        elif isinstance(slice_, slice):
            stop = Size(slice_.stop)
            if stop is None:
                stop = Size(self.width, self.height) - slice_.start

            for coord in RectRange(stop, slice_.start):
                self[coord].value = value[coord - slice_.start]

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
        """The max width."""
        return max([len(row) for row in self.rows])

    @property
    def height(self) -> int:
        return max([len(col) for col in self.cols])

    def insert(self, pos: CoordReference, cell: Cell) -> None:
        """Insert a cell at a given pos."""
        pos = Coord(pos)
        self.cells[pos.y].insert(pos.x, cell)

    def pop(self, pos: CoordReference) -> None:
        """Remove the cell at a given pos."""
        pos = Coord(pos)
        self.cells[pos.y].pop(pos.x)

    def remove(self, cell: Cell) -> None:
        """Remove the first occurrence of a cell."""
        for i, row in enumerate(self.rows):
            if cell in row:
                self.cells[i].remove(cell)

    def remove_colors(self) -> None:
        self.colors = []

    def __repr__(self) -> str:
        res = '['
        for row in self.cells:
            row_ = '['
            for cell in row:
                row_ += cell.value + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + ']'
        return res
    
    @property
    def colored_repr(self) -> str:
        res = '['
        for row in self.cells:
            row_ = '['
            for cell in row:
                row_ += str(cell.color) + cell.value + str(Color.DEFAULT) + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + str(Color.DEFAULT) + ']'
        return res

    def __str__(self) -> str:
        return "".join([str(cell.color) + repr(cell) for row in self.cells for cell in row + [Cell('\n')]])[:-1] + str(Color.DEFAULT)
    
