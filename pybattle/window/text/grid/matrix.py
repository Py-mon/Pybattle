from collections.abc import Iterable
from functools import cached_property
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    Literal,
    Self,
    Type,
    Union,
    overload,
)

from pybattle.ansi.colors import Colors, ColorType
from pybattle.log.errors import OutOfBounds
from pybattle.types_ import Align, JunctionDict, flatten, is_nested, nest
from pybattle.window.colors import Color, Colors
from pybattle.window.text.frames.border.junction_table import get_junction
from pybattle.window.text.grid.point import Coord, Size
from pybattle.window.text.grid.range import (  # rect_range,
    array_rect_range,
    selection_range,
)


class Cell:
    """A Cell in a matrix"""

    def __init__(
        self,
        value: Any,
        color: Color = Colors.DEFAULT,
        collision: bool = ...,
    ) -> None:
        self._value = value

        self.collision = collision
        if self.collision is ...:
            self.collision = True
            if self.value == " ":
                self.collision = False

        self.color = color

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new):
        self._value = new

    def __repr__(self) -> str:
        return str(self.value)

    def __len__(self) -> Literal[0]:
        return 0

    @classmethod
    def from_iter(cls, itr: Iterable) -> list[Self]:
        """Create a list of cells from an iterable"""
        return [Cell(cell) for cell in itr]

    def __mul__(self, times: int) -> list[Self]:
        return [Cell(self.value, self.color) for _ in range(times)]

    def __eq__(self, to):
        return self._value == to._value


class Junction(Cell):
    """
    A Cell that is the borders of frames.
    """

    def __init__(self, dct: JunctionDict, color: Color = Colors.DEFAULT):
        super().__init__(dct, color, True)

    @property
    def value(self):
        return get_junction(self._value)

    @property
    def dct(self):
        return self._value

    @dct.setter
    def dct(self, new):
        self._value = new

    def __add__(self, junction: Self) -> Self:
        return Junction(self.dct | junction.dct, junction.color)

    def __mul__(self, times: int) -> list[Self]:
        return [Junction(self.dct, self.color) for _ in range(times)]


def format_list(lst):
    def format(lst, join_):
        if not isinstance(lst, list):
            return str(lst)

        elements = []
        for item in lst:
            elements.append(format(item, ","))

        return "[" + (join_).join(elements) + "]"

    if is_nested(lst):
        return format(lst, ",\n ")
    return format(lst, ",")


def cache_change_property(func):
    last_value = None
    last_return = None

    @property
    def wrapper(*args) -> Any:
        nonlocal last_value, last_return

        fn, changing = func(*args)
        if changing == last_value and last_return is not None:
            return last_return

        last_return = fn(changing)
        last_value = changing
        return last_return

    return wrapper


def cache_change(fn, changing):
    last_value = None
    last_return = None

    def wrapper() -> Any:
        nonlocal last_value, last_return

        if changing == last_value and last_return is not None:
            return last_return

        last_return = fn(changing)
        last_value = changing
        return last_return

    return wrapper


class Matrix:
    """
    A matrix of cells. (The main game grid)

    Used for converting data into a matrix format that is easily editable and easy to retrieve values with coordinates.
    """

    @classmethod
    def from_str(
        cls,
        string: str,
        align: Align = Align.LEFT,
    ) -> Self:
        """
        Create a matrix from a string
        >>> Matrix.from_str('123\\n456\\n')
        ... [[1,2,3],
        ...  [4,5,6]]
        """

        return cls(
            [Cell.from_iter(row) for row in string.removeprefix("\n").splitlines()],
            align=align,
        )

    @classmethod
    def from_size(cls, size: Size, fill_with: Any = " ") -> Self:
        """
        Create a filled matrix of a value that is a certain size
        >>> Matrix.from_size(size=Size(2, 3), fill_with=5)
        ... [[5,5,5],
        ...  [5,5,5]]
        """

        height, width = size
        array = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(Cell(fill_with))
            array.append(row)

        return cls(array)

    def __init__(
        self,
        cells: list[list[Cell]],
        align: Align = Align.LEFT,
    ) -> None:
        self.cells = cells

        self.alignment = align
        
        self.__size = cache_change(Size.from_list, self.cells)

        self.level_out()

        def __cells():
            self.dct: dict[Coord, Cell] = {}
            for i, row in enumerate(self.rows):
                for j, cell in enumerate(row):
                    self.dct[Coord(i, j)] = cell

        self.__dct = cache_change(__cells, self.cells)
        self.__coords = cache_change(self.size.i.rect_range, self.size.i)

    @property
    def dct(self) -> dict[Coord, Cell]:
        return self.__dct()

    @property
    def coords(self) -> list[Coord]:
        """All of the valid coordinates in the Matrix"""
        return self.__coords()

    def level_out(self) -> None:
        """
        Level out the rows of the matrix.

        Adjust the number of cells in each row of the matrix to be the same by adding blank Cells, according to the alignment
        specified during initialization.
        """

        if self.rows:
            max_length = self.size.x

            for row in self.cells:
                row_length = len(row)
                if row_length >= max_length:
                    continue

                match self.alignment:
                    case Align.LEFT:
                        row.extend(Cell(" ") * (max_length - row_length))
                    case Align.RIGHT:
                        for _ in range(max_length - row_length):
                            row.insert(0, Cell(" "))
                    case Align.CENTER:
                        for _ in range((max_length - row_length) // 2):
                            row.insert(0, Cell(" "))
                        row += Cell(" ") * ((max_length - row_length) // 2)

                # match self.alignment:
                #     case Align.LEFT:
                #         self._cells = [
                #             row + Cell(" ") * (max_length - len(row))
                #             for row in self.rows
                #         ]
                #     case Align.RIGHT:
                #         self._cells = [
                #             Cell(" ") * (max_length - len(row)) + row
                #             for row in self.rows
                #         ]
                #     case Align.CENTER:
                #         self._cells = [
                #             Cell(" ") * cut(max_length - len(row))[0]
                #             + row
                #             + Cell(" ") * cut(max_length - len(row))[1]
                #             for row in self.rows
                #         ]

    def color(self, color: Color, coords: list[Coord]) -> None:
        """Color cells in the matrix"""
        for coord in coords:
            try:
                self[coord].color = color
            except IndexError:
                raise OutOfBounds(coord, self.size)

    def color_all(self, color: Color) -> None:
        """Color the whole matrix a certain color"""
        self.color(color, self.coords)

    def __contains__(self, item: Coord | Any) -> bool:
        """Check if a coord or cell is in the Matrix"""
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
            try:
                return self.cells[item.y][item.x]
            except IndexError:
                raise OutOfBounds(item, self.size)

        elif isinstance(item, slice):
            stop = Size(*item.stop)
            if stop is None:
                stop = Size(self.size.width, self.size.height) - item.start

            # check before Index Errors and then remove the try except

            return Matrix(
                [
                    [
                        self[coord] if coord in self.size.i else Cell(" ")
                        for coord in row
                    ]
                    for row in array_rect_range(stop, item.start)
                ]
            )

        elif isinstance(item, int):
            return Matrix([self.cells[item]])

    @overload
    def __setitem__(self, coord: Coord, cell: Cell, /) -> None:
        ...

    @overload
    def __setitem__(self, slice_: slice, matrix: Self, /) -> None:
        ...

    def __setitem__(self, item, new_cells, /) -> None:
        if isinstance(item, Coord):
            try:
                self.cells[item.y][item.x] = new_cells
            except IndexError:
                raise OutOfBounds(item, self.size)

        elif isinstance(item, slice):
            stop = item.stop
            if stop is None:
                # Was Size
                stop = Size(self.size.width, self.size.height) - item.start  # ?
            stop = Size(*stop)

            for coord in stop.rect_range(item.start):
                y_offset = coord.y - self.size.i.y
                if y_offset > 0:
                    self.extend_row(y_offset)

                x_offset = coord.x - self.size.i.x
                if x_offset > 0:
                    self.extend_column(x_offset)

                self[coord] = new_cells[coord - item.start]

    def extend_row(self, n=1):
        if n < 0:
            for _ in range(-n):
                self.cells.insert(0, Cell(" ") * self.size.width)
            return

        for _ in range(n):
            self.cells.append(Cell(" ") * self.size.width)

    def extend_column(self, n=1):
        if n < 0:
            for row in self.cells:
                for _ in range(-n):
                    row.insert(0, Cell(" "))
            return

        for row in self.cells:
            for _ in range(n):
                row.append(Cell(" "))

    def overlay(self, text: Self, pos: Coord):
        self[pos : text.size.i + pos] = text

    @property
    def rows(self) -> list[list[Cell]]:
        return self.cells

    @property
    def cols(self) -> list[list[Cell]]:
        """Transposed rows"""
        return [list(col) for col in list(zip(*self.rows))]

    @property
    def size(self) -> Size:
        return self.__size()

    def __repr__(self) -> str:
        """A formatted representation of the matrix"""
        return format_list(self.cells)

    def __str__(self) -> str:
        """The colors and values of each cell joined together"""
        return "".join([str(cell) for row in self.rows for cell in row + [Cell("\n")]])[
            :-1
        ] + str(Colors.DEFAULT)


print(repr(Matrix.from_str("hello\nworld! long")))
# class Matrix:
#     """
#     A matrix of cells. (The main game grid)

#     Used for converting data into a matrix format that is easily editable and easy to retrieve values with coordinates.
#     """

#     @classmethod
#     def from_str(
#         cls,
#         string: str,
#         align: Align = Align.LEFT,
#     ) -> Self:
#         """
#         Create a matrix from a string
#         >>> Matrix.from_str('123\\n456\\n')
#         ... [[1,2,3],
#         ...  [4,5,6]]
#         """

#         return cls(
#             [Cell.from_iter(row) for row in string.removeprefix("\n").splitlines()],
#             align=align,
#         )

#     @classmethod
#     def from_size(cls, size: Size, fill_with: Any = " ") -> Self:
#         """
#         Create a filled matrix of a value that is a certain size
#         >>> Matrix.from_size(size=Size(2, 3), fill_with=5)
#         ... [[5,5,5],
#         ...  [5,5,5]]
#         """

#         height, width = size
#         array = []
#         for _ in range(height):
#             row = []
#             for _ in range(width):
#                 row.append(Cell(fill_with))
#             array.append(row)

#         return cls(array)

#     def __init__(
#         self,
#         cells: list[list[Cell]],
#         align: Align = Align.LEFT,
#     ) -> None:
#         self.cells = cells

#         self.dct = dict(zip(self.coords, self.flat_cells))

#         self.alignment = align
#         self.level_out()

#     @cache_change_property
#     def coords(self):
#         """All of the valid coordinates in the Matrix (returns -> `list[Coord]`)"""
#         return rect_range, self.size.i

#     @cache_change_property
#     def flat_cells(self):
#         return flatten, self.cells

#     def level_out(self) -> None:
#         """
#         Level out the rows of the matrix.

#         Adjust the number of cells in each row of the matrix to be the same by adding blank Cells, according to the alignment
#         specified during initialization.
#         """

#         if self.rows:
#             row_lengths = [len(row) for row in self.rows]
#             max_length = max(row_lengths)
#             if not all(length == max_length for length in row_lengths):
#                 width = max(row_lengths)

#                 def cut(n):
#                     return (n // 2, n - (n // 2))

#                 match self.alignment:
#                     case Align.LEFT:
#                         self.cells = [
#                             row + Cell(" ") * (width - len(row)) for row in self.rows
#                         ]
#                     case Align.RIGHT:
#                         self.cells = [
#                             Cell(" ") * (width - len(row)) + row for row in self.rows
#                         ]
#                     case Align.CENTER:
#                         self.cells = [
#                             Cell(" ") * cut(width - len(row))[0]
#                             + row
#                             + Cell(" ") * cut(width - len(row))[1]
#                             for row in self.rows
#                         ]

#     def color(self, color: ColorType, coords: list[Coord]) -> None:
#         """Color cells in the matrix"""
#         for coord in coords:
#             try:
#                 self[coord].color = color
#             except IndexError:
#                 raise OutOfBounds(coord, self.size)

#     def color_all(self, color: ColorType) -> None:
#         """Color the whole matrix a certain color"""
#         self.color(color, self.coords)

#     def __contains__(self, item: Coord | Any) -> bool:
#         """Check if a coord or cell is in the Matrix"""
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
#             try:
#                 return self.rows[item.y][item.x]
#             except IndexError:
#                 raise OutOfBounds(item, self.size)

#         elif isinstance(item, slice):
#             stop = Size(*item.stop)
#             if stop is None:
#                 stop = Size(self.size.width, self.size.height) - item.start

#             # check before Index Errors and then remove the try except

#             return Matrix(
#                 [
#                     [
#                         self[coord] if coord in self.size.i else Cell(" ")
#                         for coord in row
#                     ]
#                     for row in array_rect_range(stop, item.start)
#                 ]
#             )

#         elif isinstance(item, int):
#             return Matrix([self.cells[item]])

#     @overload
#     def __setitem__(self, coord: Coord, cell: Cell, /) -> None:
#         ...

#     @overload
#     def __setitem__(self, slice_: slice, matrix: Self, /) -> None:
#         ...

#     def __setitem__(self, item, new_cells, /) -> None:
#         if isinstance(item, Coord):
#             try:
#                 self.rows[item.y][item.x] = new_cells
#             except IndexError:
#                 raise OutOfBounds(item, self.size)

#         elif isinstance(item, slice):
#             stop = item.stop
#             if stop is None:
#                 # Was Size
#                 stop = Size(self.size.width, self.size.height) - item.start  # ?
#             stop = Size(*stop)

#             for coord in rect_range(stop, item.start):
#                 y_offset = coord.y - self.size.i.y
#                 if y_offset > 0:
#                     self.extend_row(y_offset)

#                 x_offset = coord.x - self.size.i.x
#                 if x_offset > 0:
#                     self.extend_column(x_offset)

#                 self[coord] = new_cells[coord - item.start]

#     def extend_row(self, n=1):
#         if n < 0:
#             for _ in range(-n):
#                 self.cells.insert(0, Cell(" ") * self.size.width)
#             return

#         for _ in range(n):
#             self.cells.append(Cell(" ") * self.size.width)

#     def extend_column(self, n=1):
#         if n < 0:
#             for row in self.cells:
#                 for _ in range(-n):
#                     row.insert(0, Cell(" "))
#             return

#         for row in self.cells:
#             for _ in range(n):
#                 row.append(Cell(" "))

#     def overlay(self, text: Self, pos: Coord):
#         self[pos : text.size.i + pos] = text

#     @property
#     def rows(self) -> list[list[Cell]]:
#         return self.cells

#     @property
#     def cols(self) -> list[list[Cell]]:
#         """Transposed rows"""
#         return [list(col) for col in list(zip(*self.rows))]

#     @cache_change_property
#     def size(self):
#         return Size.from_list, self.cells

#     def __repr__(self) -> str:
#         """A formatted representation of the matrix"""
#         return format_list(self.cells)

#     @property
#     def colored_repr(self) -> str:
#         """A colored representation of the matrix"""
#         return format_list(
#             [[str(cell.color) + str(cell) for cell in row] for row in self.rows]
#         )

#     def __str__(self) -> str:
#         """The colors and values of each cell joined together"""
#         return "".join([str(cell) for row in self.rows for cell in row + [Cell("\n")]])[
#             :-1
#         ] + str(Colors.DEFAULT)

#     @property
#     def uncolored_str(self):
#         """The values of each cell joined together"""
#         return "".join([str(cell) for row in self.rows for cell in row + [Cell("\n")]])[
#             :-1
#         ]


# m = Matrix.from_size(Size(15, 15), "5")

# # Takes about 1 second
# print(timeit("m[Coord(13, 13)]", number=1000000, globals={"m": m, "Coord": Coord}))

# # takes 0.00039170001400634646 seconds
# x = timeit(
#     """m.dct = dict(zip(m.coords, m.flat_cells))""",
#     number=5000,
#     globals={"m": m, "Coord": Coord},
# )

# # Takes 1.5705046000075527 seconds. Why so long??
# y = timeit(
#     """m.dct[Coord(3, 3)]""",
#     number=10000,
#     globals={"m": m, "Coord": Coord},
# )

# print(x)
# print(y)

# print(x + y)
