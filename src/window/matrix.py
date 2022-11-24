from numpy import row_stack, array


class Matrix:
    """Converts a str into a Matrix so it can be easily edited and then returned back to a str."""
    def __init__(self, str_: str, array_=None) -> None:
        if str_[-1] != '\n':
            str_ += '\n'
        self.__str = str_
        if array_ is not None:
            self._matrix = array_
        else:
            self._matrix = row_stack([array(list(row)) for row in self.__str.splitlines(True)])

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
        return "".join([char for row in self._matrix for char in row])

    @property
    def shape(self):
        return self._matrix.shape