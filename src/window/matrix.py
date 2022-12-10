from re import compile, sub

from numpy import append, array, full, insert, ravel_multi_index, row_stack

from src.types_ import CoordReference
from src.window.coord import Coord
from src.window.size import Size


def ravel(coord: CoordReference, width: int) -> int:
    return coord.y * width + coord.x


class Matrix:
    """Converts a str into a Matrix so it can be easily edited and then returned back to a str."""

    @staticmethod
    def convert_array(array_) -> str:
        array_ = append(array_, full((array_.shape[0], 1), '\n'), 1)
        return "".join([char for row in array_ for char in row])

    @staticmethod
    def array_to_matrix(array_) -> "Matrix":  # doesn't work with Self
        return Matrix(Matrix.convert_array(array_))

    def remove_and_save_ansi_codes(self) -> None:
        """Save ANSI escape characters with starting positions. Then delete them from the matrix."""
        reg = compile(r'\033\[((?:\d|;)*)([a-zA-Z])')
        self._codes = []

        # Save ANSI escape characters with starting positions
        for match in reg.finditer(self._str):
            self._codes.append([match.start(), match.group()])

        # Algorithm to correct the escape codes position
        for i in range(1, len(self._codes)):
            for j in range(0, i):
                self._codes[i][0] -= len(self._codes[j][1])

        # Delete found matches
        self._str = sub(reg, '', self._str)

    def apply_ansi_codes(self, codes: list[str]):
        """Apply ANSI escape characters to the matrix."""
        for i, (pos, code) in enumerate(codes):
            pos = Coord.convert_reference(pos)
            pos.x += i
            self.insert(pos, code)

    def insert(self, pos: CoordReference, cell: str) -> None:
        """Insert a cell into the matrix at the given position."""
        pos = Coord.convert_reference(pos)
        # Because this creates it 1D we have to use the original shape of the matrix
        index = ravel_multi_index(([pos.y], [pos.x]), self._shape)
        self._matrix = insert(self._matrix, index, cell)

    def filter_string(self) -> None:
        """Get rid of unnecessary new lines."""
        rows = self._str.split('\n')
        self._str = ''
        for row in rows:
            if row == '':
                continue

            self._str += row + '\n'

    def __init__(self, str_: str) -> None:
        self._str = str_

        self.filter_string()
        self.remove_and_save_ansi_codes()
        self._matrix = row_stack([array(list(row), object)
                                 for row in self._str.splitlines()])
        self._shape = self._matrix.shape

    def __getitem__(self, slice_):
        """(No ANSI escape characters)"""
        return self._matrix[slice_]

    def __setitem__(self, slice_, cell: str):
        self._matrix[slice_] = cell

    def __iter__(self):
        """Iterates through all the cells. (No ANSI escape characters)"""
        for row in self._matrix:
            for cell in row:
                yield cell

    def __str__(self) -> str:
        """The str with ANSI escape characters formed from the matrix."""
        self.apply_ansi_codes(self._codes)
        res = Matrix.convert_array(self._matrix)
        self.remove_and_save_ansi_codes()
        return res

    @property
    def size(self) -> Size:
        return Size(self._matrix.shape[0], self._matrix.shape[1])
