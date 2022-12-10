from src.window.color import Color
from typing import Self, Iterator, Any
from src.window.coord import Coord
from src.types_ import CoordReference, AnsiEscapeCodeOrColor
from src.window.size import Size


class Code:
    """A coord assigned to a AnsiEscapeCode or Color."""

    def __init__(self, coord: CoordReference, code: AnsiEscapeCodeOrColor) -> None:
        self.coord = Coord.convert_reference(coord)
        self.code = code

    def __iter__(self) -> None:
        return iter((self.coord, self.code))
    

class Matrix:
    def __init__(self, data: str | list[list], *codes: Code) -> None:
        self.codes = codes
        
        if isinstance(data, str):
            self.array = [[cell for cell in row] for row in data.splitlines()]
        else:
            self.array = data

        width = max([len(row) for row in self.rows])
        self.array = [row + [" "] * (width - len(row)) for row in self.rows]
        
        for (coord, code) in self.codes:
            self.insert(coord, code)

    def __iter__(self) -> Iterator:
        """Iterate through every cell."""
        for row in self.rows:
            for cell in row:
                yield cell
    
    def __contains__(self, coord_or_cell: CoordReference | Any) -> bool:
        """Check if a coord or cell is in the Matrix."""
        coord_or_cell = Coord.convert_reference(coord_or_cell)
        if isinstance(coord_or_cell, Coord):
            return coord_or_cell in [Coord(0 + col, 0 + row) for col in range(self.width + 1) for row in range(self.height + 1)]
        else:
            return coord_or_cell in iter(self)

    @property
    def rows(self) -> list[list]:
        return self.array

    @property
    def cols(self) -> list[list]:
        return [list(col) for col in list(zip(*self.rows))]
    
    @property
    def size(self) -> Size:
        return (self.height, self.width)

    @property
    def width(self) -> int:
        """The max width"""
        if self.codes:
            return max([len(row) for row in self.rows]) - 1
        else:
            return max([len(row) for row in self.rows])

    @property
    def height(self):
        return max([len(col) for col in self.cols])
    
    def insert(self, pos: CoordReference, cell: str):
        pos = Coord.convert_reference(pos)
        self.array[pos.y].insert(pos.x, cell)

    def __repr__(self) -> str:
        color = str(Color.DEFAULT)
        res = '['
        for row in self.array:
            row_ = '['
            for cell in row:
                if isinstance(cell, Color):
                    color = str(cell)
                    row_ += color
                else:
                    row_ += color + cell + str(Color.DEFAULT) + ','
            res += row_[:-1] + '],\n '
        res = res[:-3] + str(Color.DEFAULT) + ']'
        return res
    

class StrMatrix(Matrix):
    def __init__(self, data: str | Matrix | list[list[object]], *codes: list[Code]) -> None:
        if isinstance(data, str):
            if data[0] == '\n':
                data = data[1:]

        super().__init__(data, *codes)

    def __str__(self) -> str:
        return "".join([str(char) for row in self.array for char in row + ['\n']])[:-1] + str(Color.DEFAULT)


array = StrMatrix(
f'''
123
456
789
''', Code((1, 1), Color.RED), Code((3, 1), Color.BLUE))

print(array.__repr__())
print(array.height)
print(array.width)
print(array)
