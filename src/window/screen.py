from typing import Optional, Tuple
from src.types_ import CoordReference, Color
from src.window.coord import Coord
from os import system, name as os_name
from enum import Enum


class EscapeCode(Enum):
    CURSOR_MOVE_UP = 0
    CURSOR_MOVE_DOWN = 1
    CURSOR_MOVE_LEFT = 2
    CURSOR_MOVE_RIGHT = 3
    MOVE_CURSOR = 4


class EscConverter:
    """EscConverter class which acts as a mediator(logic separator)... # TODO: finish the doc

    :param code: Type of an escape code
    :param args: Sequence of escape sequence parameters
    """
    def __init__(self, code: EscapeCode | str, args: Tuple[str | int]) -> None:
        self.__code = code
        self.__args = args

    @property
    def escape_code(self) -> str | None:
        """Returns the escape code based on the escape code type. If string, returns it

        :rtype: str | None
        """
        if isinstance(self.__code, str):
            return self.__code

        match self.__code:
            case EscapeCode.CURSOR_MOVE_UP:
                return 'A'
            case EscapeCode.CURSOR_MOVE_DOWN:
                return 'B'
            case EscapeCode.CURSOR_MOVE_LEFT:
                return 'C'
            case EscapeCode.CURSOR_MOVE_RIGHT:
                return 'D'
            case EscapeCode.MOVE_CURSOR:
                return 'H'
            case _:
                return None

    @property
    def escape_args(self) -> str:
        """Returns the args of the escape sequence.

        :example: args = [12, 43] => '12;43'
        :rtype: str
        """
        return "".join([str(arg) + ';' for arg in self.__args])[:-1]


class AnsiEscapeCode:
    # TODO: Add the actual explanation to the class, try to follow: https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
    """https://en.wikipedia.org/wiki/ANSI_escape_code"""
    CSI = '\033['

    def __init__(self, code: EscapeCode | str, *args: str | int) -> None:
        print(code, args)
        converter = EscConverter(code, args)

        self.code = self.CSI + converter.escape_args + converter.escape_code
        # self.real = '\\' + self.code

    def execute(self) -> None:
        """Execute the ANSI escape code."""
        print(self.code, end='')


class Cursor:
    """https://en.wikipedia.org/wiki/ANSI_escape_code"""
    pos = Coord()

    @classmethod
    def up(cls, n: int = 1) -> AnsiEscapeCode:
        """Moves the cursor `n` cells up."""
        cls.pos.y -= 1
        return AnsiEscapeCode(EscapeCode.CURSOR_MOVE_UP, n - 1)

    @classmethod
    def down(cls, n: int = 1) -> AnsiEscapeCode:
        """Moves the cursor `n` cells down."""
        cls.pos.y += 1
        return AnsiEscapeCode(EscapeCode.CURSOR_MOVE_DOWN, n - 1)

    @classmethod
    def right(cls, n: int = 1) -> AnsiEscapeCode:
        """Moves the cursor `n` cells right."""
        cls.pos.x += 1
        return AnsiEscapeCode(EscapeCode.CURSOR_MOVE_RIGHT, n - 1)

    @classmethod
    def left(cls, n: int = 1) -> AnsiEscapeCode:
        """Moves the cursor `n` cells left."""
        cls.pos.x -= 1
        return AnsiEscapeCode(EscapeCode.CURSOR_MOVE_LEFT, n - 1)

    @classmethod
    def move(cls, pos: Coord) -> AnsiEscapeCode:
        cls.pos = pos
        return AnsiEscapeCode(EscapeCode.MOVE_CURSOR, *pos)


class Screen:
    @staticmethod
    def write(
        txt: object,
        pos: CoordReference = ...,
        color: Optional[Color] = None,
        move_cursor: bool = True
    ) -> None:
        pos = Coord.convert_reference(pos)

        txt = str(txt)

        if pos is not ...:
            Cursor.move(pos).execute()

        if color is not None:
            print(color, end='')
            
        for line in txt.splitlines():
            Cursor.left(Cursor.pos.x).execute()  # May need to change to pos.x instead of Cursor.pos.x
            print(line)

        Cursor.pos.x += txt.count('\n')
        Cursor.pos.y += len(max(txt.split('\n')))

        if not move_cursor:
            Cursor.up(txt.count('\n') + 1).execute()
            
    @staticmethod
    def clear():
        """Clear the screen. Works on all operating systems."""
        system('cls' if os_name == 'nt' else 'clear')
