"""Converts a str into a Matrix so it can be easily edited and then returned back to a str."""
import re

from numpy import row_stack, array, insert
from src.window.size import Size
from re import search

class Matrix:
    """Converts a str into a Matrix so it can be easily edited and then returned back to a str."""

    @staticmethod
    def convert_array(array_) -> str:
        return "".join([char for row in array_ for char in row])

    def __init__(self, str_: str) -> None:
        self._str = str_
        self._codes = []
        self._matrix = None
        self.init_matrix()

    def init_matrix(self):
        self.filter_string()
        self.remove_and_save_escape_chars()
        self._matrix = row_stack([array(list(row)) for row in self._str.splitlines(True)])
        # Apply escape characters after numpy array was initialized to avoid size error.
        self.apply_escape_chars()

    def remove_and_save_escape_chars(self) -> None:
        reg = re.compile(r'\033\[((?:\d|;)*)([a-zA-Z])')
        self._codes = []

        for match in reg.finditer(self._str):
            # Save start position and escape seq
            self._codes.append([match.start(), match.group()])

        # Algorithm to correct the escape codes position
        for i in range(1, len(self._codes)):
            for j in range(0, i):
                self._codes[i][0] -= len(self._codes[j][1])

        # Deletes found matches
        new_str = re.sub(reg, '', self._str)
        self._str = new_str

    def apply_escape_chars(self):
        """ Applying saved escape characters to numpy matrix """

        # Offset is needed to keep track of the size of the escape sequence and increase position respectively
        offset = 0
        for (pos, escape_code) in self._codes:
            # Convert escape code to insertable format (Meaning you can only insert separated symbols)
            escape_code = list(escape_code)
            pos += offset
            for char in escape_code:
                self._matrix = insert(self._matrix, pos, char)
                # Increasing the pos to insert sequentially
                pos += 1
                offset += 1

    def filter_string(self) -> None:
        """ Get rid of unnecessary new lines"""
        rows = list(self._str.split('\n'))
        new_string = ''
        for row in rows:
            if row == '':
                continue

            new_string += row + '\n'

        self._str = new_string

    def print_char_array(self):
        """ Prints characters array. Convenient for debugging. """
        rows = list(self._str.split('\n'))
        for row in rows:
            if row == '':
                continue
            print('[ ', end='')
            for col in row:
                print(col, end=', ')
            print(' ]', end='\n')

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
