from copy import copy
from os import name as os_name
from os import system
from shutil import get_terminal_size
from time import sleep
from typing import Any, Callable, Optional

from pybattle.ansi.colors import ColorType
from pybattle.ansi.cursor import Cursor
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size


class Screen:
    @staticmethod
    def clear() -> None:
        """Clear the screen on any operating systems"""
        system("cls" if os_name == "nt" else "clear")

    @staticmethod
    def terminal_size() -> Size:
        return Size(*get_terminal_size())

    @classmethod
    def rect_print(cls, text: Any, pos: Coord = ...) -> None:
        """
        Print multiple lines on the same x axis (making a rectangle).

        Normal Printing at `Coord(0, 2)`:
        ```
          hello
        world
        ```
        Rect Printing at `Coord(0, 2)`:
        ```
          hello
          world
        """
        pos = copy(pos)
        if pos is ...:
            pos = Cursor.pos

        for line in str(text).splitlines():
            Cursor.move(pos)
            print(line)
            pos.y += 1
