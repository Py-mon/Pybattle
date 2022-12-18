from enum import Enum
from os import name as os_name
from os import system
from typing import Optional, Tuple
from shutil import get_terminal_size

from pybattle.types_ import CoordReference
from pybattle.window.coord import Coord
from pybattle.ansi.color import Colors
from pybattle.ansi.ansi import AnsiEscSeq, CursorCode
from pybattle.window.size import Size


class Cursor:
    """Keeps track of the cursor pos."""
    pos = Coord()

    @classmethod
    def up(cls, n: int = 1) -> AnsiEscSeq:
        """Moves the cursor `n` cells up."""
        cls.pos.y -= 1
        return AnsiEscSeq(CursorCode.UP, n - 1)

    @classmethod
    def down(cls, n: int = 1) -> AnsiEscSeq:
        """Moves the cursor `n` cells down."""
        cls.pos.y += 1
        return AnsiEscSeq(CursorCode.DOWN, n - 1)

    @classmethod
    def right(cls, n: int = 1) -> AnsiEscSeq:
        """Moves the cursor `n` cells right."""
        cls.pos.x += 1
        return AnsiEscSeq(CursorCode.RIGHT, n - 1)

    @classmethod
    def left(cls, n: int = 1) -> AnsiEscSeq:
        """Moves the cursor `n` cells left."""
        cls.pos.x -= 1
        return AnsiEscSeq(CursorCode.LEFT, n - 1)

    @classmethod
    def move(cls, pos: CoordReference) -> AnsiEscSeq:
        """Moves the cursor to the given pos."""
        pos = Coord.convert_reference(pos)
        cls.pos = pos
        return AnsiEscSeq(CursorCode.MOVE, *pos)


class Screen:
    @staticmethod
    def write(
        txt: object,
        pos: CoordReference = ...,
        color: Optional[Colors] = None,
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
    def clear() -> None:
        """Clear the screen. Works on all operating systems."""
        system('cls' if os_name == 'nt' else 'clear')
    
    @property
    @staticmethod
    def terminal_size() -> Size:
       return Size(get_terminal_size())

