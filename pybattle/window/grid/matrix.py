from operator import itemgetter
from typing import Generator, Self, overload, Optional, Any, Iterator, Callable

from pybattle.ansi.colors import ColorType, Colors
from pybattle.debug.log import Logger
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.range import RectRange, SelectionRange
from pybattle.window.grid.size import Size
from pybattle.window.frames.conjunctions import Conjunction
from copy import copy


class Cell:
    def __new__(cls, value, *_, **__):
        if isinstance(value, Cell):
            return value
        return super().__new__(cls)
    
    def __init__(self, value: Any, color: ColorType = Colors.DEFAULT, conjunction: Optional[Conjunction] = None) -> None:      
        if value is self:
            return
        
        self.value = value
        self.color = color
        
        self.conjunction = conjunction
        if self.conjunction is None:
            self.conjunction = {}
        
    def __repr__(self) -> str:
        return str(self.value)
    
    def __mul__(self, times: int) -> list[Self]:
        return [Cell(self.value, self.color, self.conjunction) for _ in range(times)]


class Matrix:  
    @overload
    def __init__(self, size: Size, /, *colors: tuple[Coord, ColorType]) -> None: ...
    
    @overload
    def __init__(self, string: str, /, *colors: tuple[Coord, ColorType]) -> None: ...
    
    @overload
    def __init__(self, list: list[Any], /, *colors: tuple[Coord, ColorType]) -> None: ...
    
    @overload
    def __init__(self, nested_list: list[list[Any]], /, *colors: tuple[Coord, ColorType]) -> None: ...
    
    def __init__(self, data, /, *colors: tuple[Coord, ColorType]) -> None:     
        cells = lambda row: [Cell(value) for value in row]
        
        if isinstance(data, str):
            if data[0] == '\n':
                data = data[1:]
            self.cells = [cells(row) for row in data.splitlines()]
            
        elif isinstance(data, list):
           self.cells = [cells(row) if hasattr(row, '__iter__') else cells([row]) for row in data]
        
        elif isinstance(data, (Size, Coord, tuple)):
            self.cells = self.create_empty_array(*data)
        else:
            raise TypeError(f'Invalid Type of {type(data)}: {data}')

        self.level_out()
        
        self.colors = []
        self.add_colors(*colors)
    
    create_empty_cells = lambda self, amount: Cell(' ') * amount
    create_empty_array = lambda self, height, width: [self.create_empty_cells(width) for _ in range(height)]
            
    def level_out(self):
        """Level out the matrix so that all the widths are the same."""
        if self.rows:
            row_lengths = [len(row) for row in self.rows]
            if row_lengths.count(row_lengths[0]) != len(row_lengths):
                width = max(row_lengths)
                self.cells = [row + self.create_empty_cells(width - len(row)) for row in self.rows]
        
    def next_color(self, coord: Coord) -> Coord:
        """Lexicographically find the next coord where a color is. Returns the size if there are none beyond it."""
        # If there are no colors then there are no more colors beyond it
        if len(self.colors) == 0:
            return self.size
        
        color_coords = [color_coord[0] for color_coord in self.colors]

        if coord not in color_coords:
             color_coords.append(coord)

        color_coords.sort()
        
        if coord == color_coords[-1]:
            return self.size

        index = color_coords.index(coord) + 1
        
        coord = copy(color_coords[index])
        coord.x -= 1
        
        return coord

    def add_color(self, coord: Coord, color: ColorType) -> None:
        self.colors.append((coord, color))
        for coord in SelectionRange(self.width, self.next_color(coord), coord):
            self[coord].color = color
            
    def add_colors(self, *colors: tuple[Coord, ColorType]) -> None:
        for coord, color in colors:
            self.add_color(coord, color)
            
    def add_rect_color(self, coord: Coord, color: ColorType) -> None:
        for coord in RectRange(self.next_color(coord), coord):
            self[coord].color = color

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
            return Cell(item) in iter(self)

    def __iter__(self) -> Generator[Cell, None, None]:
        """Iterate through every cell."""
        for row in self.rows:
            for cell in row:
                yield cell 
                
    def coords_for(self, cell: Coord | slice) -> Iterator[Coord]:
        if isinstance(cell, Coord):
            yield cell
            return
        stop = Size(cell.stop)
        if stop is None:
            stop = Size(self.width, self.height) - cell.start
        yield from RectRange(stop, cell.start)
                
    @overload
    def __getitem__(self, row: int, /) -> Self: ...
    
    @overload
    def __getitem__(self, slice_: slice, /) -> Self: ...

    @overload
    def __getitem__(self, coord: Coord, /) -> Cell: ...
    
    def __getitem__(self, item, /):
        """
        ```
        matrix[Coord(x, y)] -> Cell at (x, y)
        matrix[Coord(y, x):Coord(y, x)] -> Matrix from Coord(y, x) to Coord(y, x)
        """
        if isinstance(item, Coord):
            return self.cells[item.y][item.x]

        elif isinstance(item, slice):
            stop = Size(item.stop)
            if stop is None:
                stop = Size(self.width, self.height) - item.start

            return Matrix([[self[coord] for coord in row] for row in RectRange(stop, item.start).array_coords])
        
        elif isinstance(item, int):
            return Matrix(self.cells[item])

    @overload
    def __setitem__(self, coord: Coord, cell: Cell, /) -> None: ...
    
    @overload
    def __setitem__(self, slice_: slice, matrix: Self, /) -> None: ...

    def __setitem__(self, cells, new_cells, /) -> None:
        if isinstance(cells, Coord):
            self.cells[cells.y][cells.x] = new_cells

        elif isinstance(cells, slice):
            stop = Size(cells.stop)
            if stop is None:
                stop = Size(self.width, self.height) - cells.start

            for coord in RectRange(stop, cells.start):
                self[coord].value = new_cells[coord - cells.start].value
                self[coord].color = new_cells[coord - cells.start].color
                self[coord].conjunction = new_cells[coord - cells.start].conjunction

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
                row_ += str(cell.color) + cell.value + str(Colors.DEFAULT) + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + str(Colors.DEFAULT) + ']'
        return res

    def __str__(self) -> str:
        return "".join([str(cell.color) + repr(cell) for row in self.cells for cell in row + [Cell('\n')]])[:-1] + str(Colors.DEFAULT)
    
