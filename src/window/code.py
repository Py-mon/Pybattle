from src.types_ import AnsiEscapeCodeOrColor, CoordReference
from src.window.coord import Coord
from src.window.matrix import Matrix


class Code:
    """A coord assigned to a AnsiEscapeCode or Color."""

    def __init__(self, coord: CoordReference, code: AnsiEscapeCodeOrColor) -> None:
        self.coord = Coord.convert_reference(coord)
        self.code = code

    def __iter__(self) -> None:
        return iter((self.coord, self.code))


def str_with_text(str_: str, *codes: Code) -> str:
    matrix = Matrix(str_)

    matrix.apply_ansi_codes(codes)

    print(matrix._matrix)

    return str(matrix)
