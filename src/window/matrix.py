"""Converts a str into a Matrix so it can be easily edited and then returned back to a str."""

from re import compile, sub

from numpy import array, row_stack, insert

from src.window.size import Size


class Matrix:
    """Converts a str into a Matrix so it can be easily edited and then returned back to a str."""

    @staticmethod
    def convert_array(array_) -> str:
        return "".join([char for row in array_ for char in row])

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
        
    def apply_ansi_codes(self):
        """Apply saved ANSI escape characters to the matrix."""
        # TODO: Add the escape code all at one time instead of each char being added separately
        
        # Offset is needed to keep track of the size of the escape sequence and increase position respectively
        offset = 0
        for (pos, escape_code) in self._codes:
            # Convert escape code to insertable format (Meaning you can only insert separated symbols)
            escape_code = list(escape_code)
            pos += offset
            for char in escape_code:
                self.insert(pos, char)
                # Increasing the pos to insert sequentially
                pos += 1
                offset += 1
    
    def insert(self, pos, cell: str) -> None:
        self._matrix = insert(self._matrix, pos, cell)

    def __init__(self, str_: str) -> None:
        self._str = str_
        
        # Makes a newline at the start and not the end (without = error)
        if self._str[0] == '\n':
            self._str = self._str[1:]
        if self._str[-1] != '\n':
            self._str = self._str + '\n'
        
        self.remove_and_save_ansi_codes()
        self._matrix = row_stack([array(list(row)) for row in self._str.splitlines(True)])

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
        self.apply_ansi_codes()
        res = Matrix.convert_array(self._matrix)
        self.remove_and_save_ansi_codes()
        return res

    @property
    def size(self) -> Size:
        return Size(self._matrix.shape[0], self._matrix.shape[1])
