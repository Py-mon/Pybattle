"""Converts a str into a Matrix so it can be easily edited and then returned back to a str."""
import re

from numpy import row_stack, array
from src.window.size import Size
from re import search

class Matrix:
    """Converts a str into a Matrix so it can be easily edited and then returned back to a str."""
    def remove_and_save_escape_chars(self):
        reg = re.compile(r'\033\[((?:\d|;)*)([a-zA-Z])')
        res = []
        new_str = re.sub(reg, '', self._str) # Deletes found matches
        self._str = new_str

        # re.sub - to remove the matches
        # for match in reg.finditer(self._str): # Iterates through found matches
        #     escape_code = match.group() # Matched sequence
        #     match_pos = match.start() # staring position of the match in a string
            # position_y = len(self._str) // match.start()
            # position_x = len(self._str) % match.start()
            # print(position_x, position_y)
            # el = (, )
            # print(el)
            # res.append(escape_code)
        # return res

    def filter_string(self):
        """ Get rid of unnecessary new lines"""
        rows = list(self._str.split('\n'))
        new_string = ''
        for row in rows:
            if row == '':
                continue

            new_string += row + '\n'

        self._str = new_string

    @staticmethod
    def convert_array(array_) -> str:
        return "".join([char for row in array_ for char in row])

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

    def __init__(self, str_: str) -> None:
        self._str = str_
        self.remove_and_save_escape_chars()
        self.filter_string()
        # self.print_char_array()
        self._matrix = row_stack([array(list(row)) for row in self._str.splitlines(True)])
        print(self._matrix)

    #
    #
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
