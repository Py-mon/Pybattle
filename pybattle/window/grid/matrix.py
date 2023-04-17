"""Takes a string and converts it to a matrix or array to create a grid that can be easily edited"""


from typing import Any, Generator, Optional, Self, overload, Iterable, Literal

from pybattle.ansi.colors import Colors, ColorType
from pybattle.types_ import Align, ColorRange, Junction
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.range import RectRange, SelectionRange
from pybattle.window.grid.size import Size, is_nested
from pybattle.debug.errors import OutOfBounds


class Cell:
    """Represents a cell in a matrix"""

    def __new__(cls, value, *_, **__):
        if isinstance(value, Cell):
            return value
        return super().__new__(cls)

    def __init__(
        self,
        value: Any,
        color: ColorType = Colors.DEFAULT,
        junction: Optional[Junction] = None,
        collision: bool = ...,
    ) -> None:
        if value is self:
            return

        self.value = value

        self.collision = collision
        if self.collision == ...:
            self.collision = True
            if self.value == " ":
                self.collision = False

        self.color = color

        self.junction = junction
        if self.junction is None:
            self.junction = {}

    def __repr__(self) -> str:
        """Return a string representation of the cell"""
        return str(self.value)

    def __mul__(self, times: int) -> list[Self]:
        """Multiply the cell by a certain number of times to create a list of cells"""
        return [Cell(self.value, self.color, self.junction) for _ in range(times)]

    def __len__(self) -> Literal[0]:
        """Return the length of the cell. (Always 0)"""
        return 0

    @classmethod
    def from_iter(cls, itr: Iterable) -> list[Self]:
        """Create a list of cells from an iterable"""
        return [Cell(cell) for cell in itr]


class Matrix:
    """Represents a matrix of cells.

    Takes an input and converts it to a matrix or array to create a grid that can be easily edited.
    """

    @classmethod
    def from_str(
        cls, string: str, *colors: ColorRange, alignment: Align = Align.LEFT
    ) -> Self:
        """Create a matrix from a string"""

        while string.startswith("\n"):
            string = string[1:]

        if string.count("\n") == 0:
            cells = Cell.from_iter(string)
        else:
            cells = [Cell.from_iter(row) for row in string.splitlines()]

        return cls(
            cells,
            *colors,
            alignment=alignment,
        )

    @classmethod
    def from_list(
        cls, lst: list | list[list], *colors: ColorRange, alignment: Align = Align.LEFT
    ) -> Self:
        """Create a matrix from a list or nested list"""

        if ...:
            ...

        return cls(
            [
                Cell.from_iter(row) if hasattr(row, "__iter__") else [Cell(row)]
                for row in lst
            ],
            *colors,
            alignment=alignment,
        )

    @classmethod
    def from_size(
        cls, size: Size, *colors: ColorRange, alignment: Align = Align.LEFT
    ) -> Self:
        """Create an empty matrix from size"""

        # 0 Edge Cases
        # x, x -> [[' ', ...], ...]
        # x, 0 -> [[], ...]
        # 0, x -> [' ', ...]
        # 0, 0 -> []

        height, width = size
        array = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(Cell(" "))
            array.append(row)

        if height == 0:
            array = Cell(" ") * width

        return cls(array, *colors, alignment=alignment)

    def __init__(
        self,
        cells: list[list[Cell]] | list[Cell],
        *colors: ColorRange,
        alignment: Align = Align.LEFT,
    ):
        self.cells = cells

        self.alignment = alignment
        self.level_out()

        self.colors: list[ColorRange] = []
        self.add_colors(*colors)

    def level_out(self) -> None:
        """
        Level out the rows of the matrix.

        Adjusts the number of cells in each row of the matrix to be the same by adding blank Cells, according to the alignment
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

    def add_color(self, color: ColorType, range_: RectRange | SelectionRange) -> None:
        """Add color to a range of cells in the matrix"""
        self.colors.append((color, range_))
        for coord in range_:
            try:
                self[coord].color = color
            except IndexError:
                raise OutOfBounds(coord, self.size)

    def add_colors(self, *colors: ColorRange) -> None:
        """Add multiple colors ranges to the matrix"""
        for color, coord in colors:
            self.add_color(color, coord)

    @property
    def coords(self) -> list[Coord]:
        """Get a flat list of all the coordinates in the matrix"""
        return list(iter(RectRange(self.size.i)))

    @property
    def array_coords(self) -> list[list[Coord]]:
        """Get a nested list of all the coordinates in the matrix"""
        return RectRange(self.size).array_coords

    def __contains__(self, item: Coord | Any) -> bool:
        """Check if a coord or cell is in the Matrix"""
        if isinstance(item, Coord):
            return item in self.coords
        else:
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

    @overload
    def __getitem__(self, rect_range: RectRange, /) -> None:
        ...

    def __getitem__(self, item, /):
        if isinstance(item, Coord):
            try:
                return self.rows[item.y][item.x]
            except IndexError:
                raise OutOfBounds(item, self.size)

        elif isinstance(item, RectRange):
            return self[item.start : item.stop]

        elif isinstance(item, slice):
            stop = Size.from_iter(item.stop)
            if stop is None:
                stop = Size(self.size.width, self.size.height) - item.start

            return Matrix(
                [
                    [self[coord] for coord in row]
                    for row in RectRange(stop, item.start).array_coords
                ]
            )

        elif isinstance(item, int):
            if is_nested(self.cells):
                return Matrix(self.cells[item])
            return Matrix([self.cells[item]])

    @overload
    def __setitem__(self, rect_range: RectRange, matrix: Self, /) -> None:
        ...

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

        elif isinstance(item, RectRange):
            self[item.start : item.stop] = new_cells

        elif isinstance(item, slice):
            stop = Size.from_iter(item.stop)
            if stop is None:
                stop = Size(self.size.width, self.size.height) - item.start

            for coord in RectRange(stop, item.start):
                self[coord] = new_cells[coord - item.start]

    @property
    def rows(self) -> list[list[Cell]]:
        if len(self.cells) > 1 and isinstance(self.cells[0], list):
            return self.cells
        else:
            return [self.cells]

    @property
    def cols(self) -> list[list[Cell]]:
        return [list(col) for col in list(zip(*self.rows))]

    @property
    def size(self) -> Size:
        return Size.from_list(self.cells)

    def insert(self, pos: Coord, cell: Cell) -> None:
        """Insert a cell at the given pos"""
        self.rows[pos.y].insert(pos.x, cell)
        self.level_out()

    def pop(self, pos: Coord) -> None:
        """Remove the cell at the given pos"""
        self.rows[pos.y].pop(pos.x)
        self.level_out()

    def remove(self, cell: Cell) -> None:
        """Remove the first occurrence of a cell"""
        for i, row in enumerate(self.rows):
            if cell in row:
                self.rows[i].remove(cell)
        self.level_out()

    def remove_colors(self) -> None:
        self.colors = []

    def __repr__(self) -> str:
        """A formatted representation of the matrix"""
        # Takes the cells and adds a \n every row
        res = "["
        for pre_char, char in zip(str(self.cells), str(self.cells)[1:]):
            # Removes dupe spaces
            if char != " " or pre_char == " ":
                res += char
                if char == "," and pre_char == "]":
                    res += "\n "

        return res

    @property
    def colored_repr(self) -> str:
        """A colored and formatted representation of the matrix"""
        res = "["
        back = 0
        for item in self.cells:
            if isinstance(item, Cell):
                res += str(item.color) + str(item) + str(Colors.DEFAULT) + ","
                back = 1
            else:
                sublist = ",".join(
                    str(cell.color) + cell.value + str(Colors.DEFAULT) for cell in item
                )
                res += f"[{sublist}],\n "
                back = 3

        res = res[:-back] + "]"
        return res

    def __str__(self) -> str:
        """The colors and values of each cell joined together"""
        return "".join(
            [
                str(cell.color) + cell.value
                for row in self.rows
                for cell in row + [Cell("\n")]
            ]
        )[:-1] + str(Colors.DEFAULT)

    @property
    def uncolored_str(self):
        """The values of each cell joined together"""
        return "".join(
            [repr(cell) for row in self.rows for cell in row + [Cell("\n")]]
        )[:-1]
