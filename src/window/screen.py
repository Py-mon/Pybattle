from enum import Enum
from os import name as os_name
from os import system
from typing import Optional, Tuple

from src.types_ import Color, CoordReference
from src.window.coord import Coord


class EscSeq(Enum):
    CURSOR_MOVE_UP = 0
    CURSOR_MOVE_DOWN = 1
    CURSOR_MOVE_LEFT = 2
    CURSOR_MOVE_RIGHT = 3
    MOVE_CURSOR = 4


class EscConverter:
    """EscConverter class which acts as a mediator (logic separator)."""

    def __init__(self, code: EscSeq | str, args: Tuple[str | int]) -> None:
        self.__code = code
        self.__args = args

    @property
    def escape_code(self) -> str:
        """Returns the escape code based on the escape code type. If string, returns it."""
        if isinstance(self.__code, str):
            return self.__code

        match self.__code:
            case EscSeq.CURSOR_MOVE_UP:
                return 'A'
            case EscSeq.CURSOR_MOVE_DOWN:
                return 'B'
            case EscSeq.CURSOR_MOVE_LEFT:
                return 'C'
            case EscSeq.CURSOR_MOVE_RIGHT:
                return 'D'
            case EscSeq.MOVE_CURSOR:
                return 'H'
            case _:
                return self.__code

    @property
    def escape_args(self) -> str:
        """Returns the args of the escape sequence.
        >>> [12, 43] -> '12;43'
        """
        return "".join([str(arg) + ';' for arg in self.__args])[:-1]


class AnsiEscSeq:
    """ANSI escape sequences are a standard for in-band signaling to control cursor location, color, font styling, and other options on terminals. 
    
    All ANSI escape sequences have a prefix; ESC (Escape).
    - Octal: \\033
    - Unicode: \\u001b
    - Hexadecimal: \\x1B (\\x1b)
    - Decimal: 27
    
    The most useful sequences start with CSI (Control Sequence Introducer)
    - ESC[
        
    For example to make the color red: ESC[31m or \\033[31m
    
    Learn more here: https://en.wikipedia.org/wiki/ANSI_escape_code"""
    ESC = '\033'
    CSI = ESC + '['

    def __init__(self, code: EscSeq | str, *args: str | int) -> None:
        converter = EscConverter(code, args)

        self.code = self.CSI + converter.escape_args + converter.escape_code

    def execute(self) -> None:
        """Execute the ANSI escape code."""
        print(self.code, end='')


class Cursor:
    """Keeps track of the cursor pos."""
    pos = Coord()

    @classmethod
    def up(cls, n: int = 1) -> AnsiEscSeq:
        """Moves the cursor `n` cells up."""
        cls.pos.y -= 1
        return AnsiEscSeq(EscSeq.CURSOR_MOVE_UP, n - 1)

    @classmethod
    def down(cls, n: int = 1) -> AnsiEscSeq:
        """Moves the cursor `n` cells down."""
        cls.pos.y += 1
        return AnsiEscSeq(EscSeq.CURSOR_MOVE_DOWN, n - 1)

    @classmethod
    def right(cls, n: int = 1) -> AnsiEscSeq:
        """Moves the cursor `n` cells right."""
        cls.pos.x += 1
        return AnsiEscSeq(EscSeq.CURSOR_MOVE_RIGHT, n - 1)

    @classmethod
    def left(cls, n: int = 1) -> AnsiEscSeq:
        """Moves the cursor `n` cells left."""
        cls.pos.x -= 1
        return AnsiEscSeq(EscSeq.CURSOR_MOVE_LEFT, n - 1)

    @classmethod
    def move(cls, pos: CoordReference) -> AnsiEscSeq:
        """Moves the cursor to the given pos."""
        pos = Coord.convert_reference(pos)
        cls.pos = pos
        return AnsiEscSeq(EscSeq.MOVE_CURSOR, *pos)


class Screen:
    @staticmethod
    def write(
        txt: object,
        pos: CoordReference = ...,
        color: Optional[Color] = None,
        move_cursor: bool = True
    ) -> None:
        """Print text to the screen."""
        pos = Coord.convert_reference(pos)

        txt = str(txt)

        if pos is not ...:
            Cursor.move(pos).execute()

        if color is not None:
            print(color, end='')

        for line in txt.splitlines():
            print(line)

        Cursor.pos.x += txt.count('\n')
        Cursor.pos.y += len(max(txt.split('\n')))

        if not move_cursor:
            Cursor.up(txt.count('\n') + 1).execute()

    @staticmethod
    def clear():
        """Clear the screen. Works on all operating systems."""
        system('cls' if os_name == 'nt' else 'clear')

    @staticmethod
    def change_scene(scene: str):
        Screen.clear()
        Screen.write(scene)
