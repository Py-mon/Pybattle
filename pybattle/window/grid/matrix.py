from collections.abc import Iterable
from typing import Any, Generator, Iterable, Literal, Self, overload

from pybattle.ansi.colors import Colors, ColorType
from pybattle.log.errors import OutOfBounds
from pybattle.types_ import Align, JunctionDict, is_nested, nest
from pybattle.window.frames.border.junction_table import get_junction
from pybattle.window.grid.coord import Coord


from pybattle.window.grid.range import selection_range, rect_range, array_rect_range
from pybattle.window.grid.size import Size


class Cell:
    """A Cell in a matrix"""

    def __init__(
        self,
        value: Any,
        color: ColorType = Colors.DEFAULT,
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

    def __str__(self) -> str:
        return str(self.color) + str(self.value)

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

    def __init__(self, dct: JunctionDict, color: ColorType = Colors.DEFAULT):
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

        return (
            str(Colors.DEFAULT)
            + "["
            + (str(Colors.DEFAULT) + join_).join(elements)
            + str(Colors.DEFAULT)
            + "]"
        )

    if is_nested(lst):
        return format(lst, ",\n ")
    return format(lst, ",")


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
        >>> Matrix.from_size(Size(2, 3), 5)
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
        self.level_out()

        self.colors: list[ColorRange] = []

    @property
    def coords(self) -> list[Coord]:
        """All of the valid coordinates in the Matrix"""
        return rect_range(self.size.i)

    def level_out(self) -> None:
        """
        Level out the rows of the matrix.

        Adjust the number of cells in each row of the matrix to be the same by adding blank Cells, according to the alignment
        specified during initialization.
        """
        if self.rows:
            row_lengths = [len(row) for row in self.rows]
            max_length = max(row_lengths)
            if not all(length == max_length for length in row_lengths):
                width = max(row_lengths)

                def cut(n):
                    return (n // 2, n - (n // 2))

                match self.alignment:
                    case Align.LEFT:
                        self.cells = [
                            row + Cell(" ") * (width - len(row)) for row in self.rows
                        ]
                    case Align.RIGHT:
                        self.cells = [
                            Cell(" ") * (width - len(row)) + row for row in self.rows
                        ]
                    case Align.CENTER:
                        self.cells = [
                            Cell(" ") * cut(width - len(row))[0]
                            + row
                            + Cell(" ") * cut(width - len(row))[1]
                            for row in self.rows
                        ]

    def color(self, color: ColorType, coords: list[Coord]) -> None:
        """Color cells in the matrix"""
        for coord in coords:
            try:
                self[coord].color = color
            except IndexError:
                raise OutOfBounds(coord, self.size)

    def color_all(self, color: ColorType) -> None:
        """Color the whole matrix a certain color"""
        self.color(color, rect_range(self.size.i))

    @property
    def coords(self) -> list[Coord]:
        """Get a nested list of all the coordinates in the matrix"""
        return rect_range(self.size)

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
                return self.rows[item.y][item.x]
            except IndexError:
                raise OutOfBounds(item, self.size)

        elif isinstance(item, slice):
            stop = Size(*item.stop)
            if stop is None:
                stop = Size(self.size.width, self.size.height) - item.start

            return Matrix(
                [
                    [self[coord] for coord in row]
                    for row in array_rect_range(stop, item.start)
                ]
            )

        elif isinstance(item, int):
            return Matrix(nest(self.cells[item])[0])
            #! If errors try this instead
            # if is_nested(self.cells):
            #     return Matrix(self.cells[item])
            # return Matrix([self.cells[item]])

    @overload
    def __setitem__(self, coord: Coord, cell: Cell, /) -> None:
        ...

    @overload
    def __setitem__(self, slice_: slice, matrix: Self, /) -> None:
        ...

    def __setitem__(self, item, new_cells, /) -> None:
        if isinstance(item, Coord):
            try:
                self.rows[item.y][item.x] = new_cells
            except IndexError:
                raise OutOfBounds(item, self.size)

        elif isinstance(item, slice):
            stop = item.stop
            if stop is None:
                stop = Size(self.size.width, self.size.height) - item.start  # ?
            stop = Size(*stop)

            for coord in rect_range(stop, item.start):
                self[coord] = new_cells[coord - item.start]

    @property
    def rows(self) -> list[list[Cell]]:
        return self.cells

    @property
    def cols(self) -> list[list[Cell]]:
        """Transposed rows"""
        return [list(col) for col in list(zip(*self.rows))]

    @property
    def size(self) -> Size:
        return Size.from_list(self.cells)

    def __repr__(self) -> str:
        """A formatted representation of the matrix"""
        return format_list(self.cells)

    @property
    def colored_repr(self) -> str:
        """A colored representation of the matrix"""
        return format_list(
            [[str(cell.color) + str(cell) for cell in row] for row in self.rows]
        )

    def __str__(self) -> str:
        """The colors and values of each cell joined together"""
        return "".join([str(cell) for row in self.rows for cell in row + [Cell("\n")]])[
            :-1
        ] + str(Colors.DEFAULT)

    @property
    def uncolored_str(self):
        """The values of each cell joined together"""
        return "".join([str(cell) for row in self.rows for cell in row + [Cell("\n")]])[
            :-1
        ]
