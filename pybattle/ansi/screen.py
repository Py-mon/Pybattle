from os import name as os_name
from os import system
from shutil import get_terminal_size
from typing import Optional

from pybattle.ansi.cursor import Cursor
from pybattle.ansi.colors import ColorType
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size


class Screen:
    @staticmethod
    def write(
        txt: object,
        pos: Coord = ...,
        color: Optional[ColorType] = None,
        move_cursor: bool = True
    ) -> None:
        """Print text to the screen."""
        txt = str(txt)

        if pos is not ...:
            Cursor.move(pos)

        if color is not None:
            print(color, end='')

        for line in txt.splitlines():
            print(line)

        Cursor.pos.x += txt.count('\n')
        Cursor.pos.y += len(max(txt.split('\n')))

        if move_cursor:
            Cursor.up(txt.count('\n') + 2)

    @staticmethod
    def clear() -> None:
        """Clear the screen. Works on all operating systems."""
        system('cls' if os_name == 'nt' else 'clear')

    @staticmethod
    def terminal_size() -> Size:
        return Size(get_terminal_size())
