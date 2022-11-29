"""Converts a str into a Matrix so it can be easily edited and then returned back to a str."""

from re import compile, sub

from numpy import array, row_stack

from src.window.size import Size


class Matrix:
    """Converts a str into a Matrix so it can be easily edited and then returned back to a str."""

    @staticmethod
    def convert_array(array_) -> str:
        return "".join([char for row in array_ for char in row])

    def __init__(self, str_: str) -> None:
        self._str = str_
        
        reg = compile(r'\xb1\[((?:\d|;)*)([a-zA-Z])')
        self._str = sub(reg, '', self._str) # Deletes found matches
        
        print(self._str)
        
        # TODO: Fix (colors is always {})
        colors: dict[str, tuple[int, int]] = {}
        for match in reg.finditer(self._str): # Iterates through found matches
            escape_code = match.group() # Matched sequence
            y = len(self._str) // match.start()
            x = len(self._str) % match.start()
            colors[escape_code] = (x, y)
        
        rows = self._str.split('\n')
        self._str = ''
        for row in rows:
            if row != '':
                self._str += row + '\n'
        
        self._matrix = row_stack([array(list(row)) for row in self._str.splitlines(True)])

        for color, location in colors.items():
            self._matrix[location] = color + self._matrix[location]
        
        print(self._matrix)

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
