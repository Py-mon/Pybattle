from collections.abc import Iterable
from copy import copy, deepcopy
from functools import cache
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Literal,
    Optional,
    Self,
    Type,
    Union,
    overload,
)

from pybattle.log.errors import OutOfBounds, TooSmallError
from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.border.junction_table import get_junction
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.nested import (
    flatten,
    format,
    is_nested,
    level_out,
    max_len,
    nest,
)
from pybattle.screen.grid.point import Coord, Point, Size
from pybattle.types_ import Alignment, Direction, JunctionDict


class Junction(Cell):
    """A Cell that is the borders of frames."""

    def __init__(self, dct: JunctionDict, color: Color = Colors.DEFAULT):
        super().__init__(dct, color, True)

    @property
    def value(self):
        return get_junction(self._value)

    @property
    def dct(self):
        return self._value

    def __add__(self, junction: Self) -> Self:
        return Junction(self.dct | junction.dct, junction.color)

    def __mul__(self, times: int) -> tuple[Self, ...]:
        return tuple(Junction(self.dct, self.color) for _ in range(times))


class Matrix:
    """
    A matrix of cells. (The main game grid)

    Used for converting data into a matrix format that is easily editable and easy to retrieve values with coordinates.
    """

    def __init__(
        self,
        cells: tuple[tuple[Cell, ...], ...],
        alignment: Optional[Alignment] = Alignment.LEFT,
    ) -> None:
        self.cells = cells

        @cache
        def __size(cells):
            return Size.from_iter(cells)

        self.__size = __size

        if alignment:
            self.level_out(alignment)

        @cache
        def _dct(cells):
            dct: dict[Coord, Cell] = {}
            for i, row in enumerate(cells):
                for j, cell in enumerate(row):
                    dct[Coord(i, j)] = cell
            return dct

        self.__dct = _dct

        @cache
        def _dct_rows(cells):
            lst: list[dict[Coord, Cell]] = []
            for i, row in enumerate(cells):
                dct: dict[Coord, Cell] = {}
                for j, cell in enumerate(row):
                    dct[Coord(i, j)] = cell
                lst.append(dct)
            return lst

        self.__dct_rows = _dct_rows

        @cache
        def __coords(cells):
            return self.size.i.rect_range()

        # Can also do (I Think)
        # @cache
        # def __coords(_):
        #     return self.size.i.rect_range, self.size.i

        self.__coords = __coords

        @cache
        def __str(cells):
            return "".join(
                tuple(
                    str(cell.value) for row in cells for cell in (row + (Cell("\n"),))
                )
            )[:-1]

        self.__str = __str

    @property
    def dct(self) -> dict[Coord, Cell]:
        return self.__dct(self.cells)

    @property
    def dct_rows(self) -> list[dict[Coord, Cell]]:
        return self.__dct_rows(self.cells)

    @property
    def coords(self):
        """All of the valid coordinates in the Matrix."""
        return self.__coords(self.cells)

    def level_out(self, alignment: Alignment = Alignment.LEFT) -> None:
        """Level out the rows of the matrix making them all the same width."""
        if self.cells:
            self.cells = level_out(self.cells, alignment)

    def color(self, color: Color, coords: list[Coord]) -> None:
        """Color cells in the matrix."""
        for coord in coords:
            if coord not in self.size:
                raise OutOfBounds(
                    f"The color '{color.name}' at {coord} is out of bounds of {self.size.i} by {(coord - self.size.i).non_negative}"
                )
            self[coord].color = color

    def color_all(self, color: Color) -> None:
        """Color the whole matrix a certain color."""
        self.color(color, self.coords)

    def __contains__(self, item: Coord | Any) -> bool:
        """Check if a coord or cell is in the Matrix."""
        if isinstance(item, Coord):
            return item in self.coords
        return Cell(item) in self

    def __iter__(self) -> Generator[Cell, None, None]:
        """Iterate through every cell"""
        for row in self.rows:
            for cell in row:
                yield cell

    @overload
    def __getitem__(self, row: int, /) -> Self:
        ...

    @overload
    def __getitem__(self, slice_: slice, /) -> Self:
        ...

    @overload
    def __getitem__(self, coord: Coord, /) -> Cell:
        ...

    def __getitem__(self, item, /):
        if isinstance(item, Coord):
            # if item not in self.size:
            #     raise OutOfBounds(
            #         f"{item} is out of bounds of {self.size.i} by {(item - self.size.i).non_negative}"
            #     )

            return self.cells[item.y][item.x]

        elif isinstance(item, slice):
            if item.stop is None:
                stop = Size(self.size.width, self.size.height) - item.start
            else:
                stop = Size(*item.stop)

            # if not self.size.within(stop, item.start):
            #     raise OutOfBounds  # TODO

            return Matrix(
                tuple(
                    tuple(
                        self[coord]  # if coord in self.size else Cell(" ")
                        for coord in row
                    )
                    for row in stop.array_rect_range(item.start)
                )
            )

        elif isinstance(item, int):
            return Matrix((self.cells[item],))

    @overload
    def __setitem__(self, coord: Coord, cell: Cell, /) -> None:
        ...

    @overload
    def __setitem__(self, slice_: slice, matrix, /) -> None:
        ...

    @overload
    def __setitem__(self, tup: tuple, value: Any, /) -> None:
        ...

    def __setitem__(self, item, new_cells, /) -> None:
        if isinstance(item, Coord):
            if item not in self.size:
                raise OutOfBounds

            cells = [list(row) for row in self.cells]
            cells[item.y][item.x] = new_cells

            self.cells = tuple(tuple(row) for row in cells)

            # self.cells = self[:item].cells + (new_cells,) + self[item:].cells

            # self.cells[item.y][item.x]._value = new_cells._value
            # self.cells[item.y][item.x].color = new_cells.color
            # self.cells[item.y][item.x].collision = new_cells.collision

        elif isinstance(item, slice):
            start = item.start or Size(0, 0)
            stop = Size(item.stop.y, item.stop.x) or (self.size.i - start)

            # if not self.size.within(stop, start):
            #     raise OutOfBounds

            cells = [list(row) for row in self.cells]

            for coord in stop.rect_range(start):
                # y_offset = coord.y - self.size.i.y
                # x_offset = coord.x - self.size.i.x

                # if y_offset > 0:
                #     self.extend_row(cells, y_offset)
                # if x_offset > 0:
                #     self.extend_column(cells, x_offset)

                cells[coord.y][coord.x] = new_cells[coord - start]

            self.cells = tuple(tuple(row) for row in cells)

            # start = item.start
            # if start is None:
            #     start = Size(0, 0)

            # if item.stop is None:
            #     stop = self.size - start  # ?
            #     stop = self.size.i - start  # ?
            # else:
            #     stop = Size(*item.stop)

            # start = item.start or Size(0, 0)
            # stop = item.stop or (self.size.i - start)

            # if not self.size.within(stop, start):
            #     raise OutOfBounds

            # for coord in stop.rect_range(start):
            #     y_offset = coord.y - self.size.i.y
            #     if y_offset > 0:
            #         self.extend_row(None, y_offset)

            #     x_offset = coord.x - self.size.i.x
            #     if x_offset > 0:
            #         self.extend_column(None, x_offset)

            #     self[coord] = new_cells[coord - start]

    def extend_row(self, with_: Optional[tuple] = None, n: int = 1):
        """Extend `n` row(s) of spaces (if negative extends the opposite way)"""
        if with_ is None:
            with_ = Cell(" ") * self.size.width

        if n < 0:
            self.cells = (with_,) * (-n) + self.cells
        else:
            self.cells = self.cells + (with_,) * n

        self.level_out()

    def extend_column(self, with_: Optional[tuple] = None, n: int = 1):
        """Extend `n` column(s) of spaces (if negative extends the opposite way)"""
        if with_ is None:
            with_ = Cell(" ") * self.size.height

        if n < 0:
            self.cells = tuple(
                tuple(with_[i] for _ in range(-n)) + row
                for i, row in enumerate(self.cells)
            )
        else:
            self.cells = tuple(
                row + tuple(with_[i] for _ in range(n))
                for i, row in enumerate(self.cells)
            )

    def overlay(self, text, pos: Coord):
        """Overlay a Matrix on top of this Matrix (the `pos` starts at the Matrix's top left corner)"""
        self[pos : text.size.i + pos] = text

    @property
    def rows(self) -> tuple[tuple[Cell, ...], ...]:
        """The same as `self.cells` (for readability in for loops: `for row in matrix.rows`)"""
        return self.cells

    @property
    def cols(self) -> list[list[Cell]]:
        """Transposed rows."""
        return [list(col) for col in list(zip(*self.rows))]

    @property
    def size(self) -> Size:
        """The height and width of the Matrix."""
        return self.__size(self.cells)

    def __repr__(self) -> str:
        """A formatted representation of the matrix."""
        return format(self.cells)

    def __str__(self) -> str:
        """The colors and values of each cell joined together."""
        return self.__str(self.cells)

    def remove_whitespace_sides(self):
        matrix = list(self.cells)

        while all(row[1].value == " " for row in matrix):
            for i in range(len(matrix)):
                matrix[i] = matrix[i][2:]

        # Remove leading space rows
        while matrix[0] and all(
            matrix[0][i].value == " " for i in range(len(matrix[0]))
        ):
            matrix.pop(0)

        # Remove trailing space rows
        while matrix[-1] and all(
            matrix[-1][i].value == " " for i in range(len(matrix[-1]))
        ):
            matrix.pop()

        self.cells = tuple(matrix)


# m = Matrix(((Cell(1), Cell(1)), (Cell(1),)))


# print(repr(m))
# print(m.size)
# m.cells = m.cells[:-1]

# print(m.size)

# from collections.abc import Iterable
# from copy import copy, deepcopy
# from typing import (
#     Any,
#     Callable,
#     Generator,
#     Iterable,
#     Literal,
#     Optional,
#     Self,
#     Type,
#     Union,
#     overload,
# )

# from pybattle.log.errors import OutOfBounds, TooSmallError
# from pybattle.screen.colors import Color, Colors
# from pybattle.screen.frames.border.junction_table import get_junction
# from pybattle.screen.grid.cell import Cell
# from pybattle.screen.grid.nested import (
#     flatten,
#     format_list,
#     is_nested,
#     level_out,
#     nest,
#     nested_len,
# )
# from pybattle.screen.grid.point import Coord, Point, Size
# from pybattle.types_ import Alignment, Direction, JunctionDict


# class Junction(Cell):
#     """A Cell that is the borders of frames."""

#     def __init__(self, dct: JunctionDict, color: Color = Colors.DEFAULT):
#         super().__init__(dct, color, True)

#     @property
#     def value(self):
#         return get_junction(self._value)

#     @property
#     def dct(self):
#         return self._value

#     def __add__(self, junction: Self) -> Self:
#         return Junction(self.dct | junction.dct, junction.color)

#     def __mul__(self, times: int) -> list[Self]:
#         return [Junction(self.dct, self.color) for _ in range(times)]


# def cache_change(fn, value_changing):
#     """Save the result and only rerun the function when the value changes."""
#     last_value = None
#     last_return = None
#     copy_change = value_changing

#     def wrapper() -> Any:
#         nonlocal last_value, last_return, copy_change

#         if copy_change == last_value and last_return is not None:
#             return last_return

#         last_return = fn(value_changing)
#         last_value = value_changing

#         copy_change = deepcopy(value_changing)
#         return last_return

#     return wrapper


# class Matrix:
#     """
#     A matrix of cells. (The main game grid)

#     Used for converting data into a matrix format that is easily editable and easy to retrieve values with coordinates.
#     """

#     def __init__(
#         self,
#         cells: list[list[Cell]],
#         alignment: Alignment = Alignment.LEFT,
#     ) -> None:
#         self.cells = cells

#         self._size = cache_change(Size.from_list, self.cells)

#         self.level_out(alignment)

#         def __dct(_):
#             dct: dict[Coord, Cell] = {}
#             for i, row in enumerate(self.rows):
#                 for j, cell in enumerate(row):
#                     dct[Coord(i, j)] = cell
#             return dct

#         self.__dct = cache_change(__dct, self.cells)

#         def __dct_rows(_):
#             lst: list[dict[Coord, Cell]] = []
#             for i, row in enumerate(self.rows):
#                 dct: dict[Coord, Cell] = {}
#                 for j, cell in enumerate(row):
#                     dct[Coord(i, j)] = cell
#                 lst.append(dct)
#             return lst

#         self.__dct_rows = cache_change(__dct_rows, self.cells)

#         self.__coords = cache_change(self.size.i.rect_range, self.size.i)

#         self.__str = cache_change(
#             lambda _: "".join(
#                 [cell.value for row in self.cells for cell in row + [Cell("\n")]]
#             )[:-1],
#             self.cells,
#         )

#     @property
#     def dct(self) -> dict[Coord, Cell]:
#         return self.__dct()

#     @property
#     def dct_rows(self) -> list[dict[Coord, Cell]]:
#         return self.__dct_rows()

#     @property
#     def coords(self) -> list[Coord]:
#         """All of the valid coordinates in the Matrix."""
#         return self.__coords()

#     def level_out(self, alignment: Alignment = Alignment.LEFT) -> None:
#         """Level out the rows of the matrix making them all the same width."""
#         level_out(self.cells, alignment)

#     def color(self, color: Color, coords: list[Coord]) -> None:
#         """Color cells in the matrix."""
#         for coord in coords:
#             if coord not in self.size:
#                 raise OutOfBounds(
#                     f"The color '{color.name}' at {coord} is out of bounds of {self.size.i} by {(coord - self.size.i).non_negative}"
#                 )
#             self[coord].color = color

#     def color_all(self, color: Color) -> None:
#         """Color the whole matrix a certain color."""
#         self.color(color, self.coords)

#     def __contains__(self, item: Coord | Any) -> bool:
#         """Check if a coord or cell is in the Matrix."""
#         if isinstance(item, Coord):
#             return item in self.coords
#         return Cell(item) in self

#     def __iter__(self) -> Generator[Cell, None, None]:
#         """Iterate through every cell"""
#         for row in self.rows:
#             for cell in row:
#                 yield cell

#     @overload
#     def __getitem__(self, row: int, /) -> Self:
#         ...

#     @overload
#     def __getitem__(self, slice_: slice, /) -> Self:
#         ...

#     @overload
#     def __getitem__(self, coord: Coord, /) -> Cell:
#         ...

#     def __getitem__(self, item, /):
#         if isinstance(item, Coord):
#             if item not in self.size:
#                 raise OutOfBounds(
#                     f"{item} is out of bounds of {self.size.i} by {(item - self.size.i).non_negative}"
#                 )

#             return self.cells[item.y][item.x]

#         elif isinstance(item, slice):
#             stop = Size(*item.stop)
#             if stop is None:
#                 stop = Size(self.size.width, self.size.height) - item.start

#             if not self.size.within(stop, item.start):
#                 raise OutOfBounds # TODO

#             return Matrix(
#                 [
#                     [self[coord] if coord in self.size else Cell(" ") for coord in row]
#                     for row in stop.array_rect_range(item.start)
#                 ]
#             )

#         elif isinstance(item, int):
#             return Matrix([self.cells[item]])

#     @overload
#     def __setitem__(self, coord: Coord, cell: Cell, /) -> None:
#         ...

#     @overload
#     def __setitem__(self, slice_: slice, matrix, /) -> None:
#         ...

#     @overload
#     def __setitem__(self, tup: tuple, value: Any, /) -> None:
#         ...

#     def __setitem__(self, item, new_cells, /) -> None:
#         if isinstance(item, tuple):
#             if isinstance(item[0], Coord):
#                 try:
#                     loc = self.cells[item[0].y][item[0].x]

#                     if isinstance(loc, Junction):
#                         dct = {
#                             "dct": loc.dct,
#                             "color": loc.color,
#                         }
#                         dct[item[1]] = new_cells
#                         loc = Junction(**dct)
#                     else:
#                         dct = {
#                             "value": loc.value,
#                             "color": loc.color,
#                             "collision": loc.collision,
#                         }
#                         dct[item[1]] = new_cells
#                         self.cells[item[0].y][item[0].x] = Cell(**dct)

#                 except IndexError:
#                     raise OutOfBounds

#         if isinstance(item, Coord):
#             if item not in self.size:
#                 raise OutOfBounds

#             self.cells[item.y][item.x] = new_cells

#         elif isinstance(item, slice):
#             stop = Size(*item.stop)
#             if stop is None:
#                 stop = Size(self.size.width, self.size.height) - item.start  # ?

#             if not self.size.within(stop, item.start):
#                 raise OutOfBounds

#             for coord in stop.rect_range(item.start):
#                 y_offset = coord.y - self.size.i.y
#                 if y_offset > 0:
#                     self.extend_row(y_offset)

#                 x_offset = coord.x - self.size.i.x
#                 if x_offset > 0:
#                     self.extend_column(x_offset)

#                 self[coord] = new_cells[coord - item.start]

#     def extend_row(self, n=1):
#         """Extend `n` row(s) of spaces (if negative extends the opposite way)"""
#         if n < 0:
#             for _ in range(-n):
#                 self.cells.insert(0, Cell(" ") * self.size.width)
#             return

#         for _ in range(n):
#             self.cells.append(Cell(" ") * self.size.width)

#     def extend_column(self, n: int = 1):
#         """Extend `n` column(s) of spaces (if negative extends the opposite way)"""
#         if n < 0:
#             for row in self.cells:
#                 for _ in range(-n):
#                     row.insert(0, Cell(" "))
#             return

#         for row in self.cells:
#             for _ in range(n):
#                 row.append(Cell(" "))

#     def overlay(self, text: Self, pos: Coord):
#         """Overlay a Matrix on top of this Matrix (the `pos` starts at the Matrix's top left corner)"""
#         self[pos : text.size.i + pos] = text

#     @property
#     def rows(self) -> list[list[Cell]]:
#         """The same as `self.cells` (for readability in for loops: `for row in matrix.rows`)"""
#         return self.cells

#     @property
#     def cols(self) -> list[list[Cell]]:
#         """Transposed rows."""
#         return [list(col) for col in list(zip(*self.rows))]

#     @property
#     def size(self) -> Size:
#         """The height and width of the Matrix."""
#         return self._size()

#     def __repr__(self) -> str:
#         """A formatted representation of the matrix."""
#         return format_list(self.cells)

#     def __str__(self) -> str:
#         """The colors and values of each cell joined together."""
#         return self.__str()
