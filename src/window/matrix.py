"""Converts a str into a Matrix so it can be easily edited and then returned back to a str."""

from numpy import row_stack, array
from .size import Size


class Matrix:
    """Converts a str into a Matrix so it can be easily edited and then returned back to a str."""
    
    @staticmethod
    def convert_array(array_) -> str:
        return "".join([char for row in array_ for char in row])
        
    def __init__(self, str_: str) -> None:
        if str_[-1] != '\n':
            str_ += '\n'
        self._str = str_
        
        self._matrix = row_stack([array(list(row)) for row in self._str.splitlines(True)])

    def __len__(self) -> int:
        return len(self._matrix)

    def __getitem__(self, slice_):
        return self._matrix[slice_]

    def __setitem__(self, slice_, value: str):
        self._matrix[slice_] = value

    def __iter__(self):
        for row in self._matrix:
            yield row

    def __str__(self) -> str:
        """The str formed from the matrix."""
        return Matrix.convert_array(self._matrix)

    @property
    def size(self) -> Size:
        return Size(self._matrix.shape[0], self._matrix.shape[1])
