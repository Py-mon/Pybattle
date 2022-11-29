from typing import Optional

from src.types_ import CoordReference
from src.window.coord import Coord
from src.window.color import Color


class AnsiEscapeCode:
    """https://en.wikipedia.org/wiki/ANSI_escape_code"""
    ESC = '\033'
    CSI = ESC + '['

    def __init__(self, code: str, *args: str | int) -> None:
        self.code = self.CSI + \
            "".join([str(arg) + ';' for arg in args])[:-1] + code
        self.real = '\\' + self.code

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
        return AnsiEscapeCode('A', n - 1)

    @classmethod
    def down(cls, n: int = 1) -> AnsiEscapeCode:
        """Moves the cursor `n` cells down."""
        cls.pos.y += 1
        return AnsiEscapeCode('B', n - 1)

    @classmethod
    def right(cls, n: int = 1) -> AnsiEscapeCode:
        """Moves the cursor `n` cells right."""
        cls.pos.x += 1
        return AnsiEscapeCode('C', n - 1)

    @classmethod
    def left(cls, n: int = 1) -> AnsiEscapeCode:
        """Moves the cursor `n` cells left."""
        cls.pos.x -= 1
        return AnsiEscapeCode('D', n - 1)

    @classmethod
    def move(cls, pos: Coord) -> AnsiEscapeCode:
        cls.pos = pos
        return AnsiEscapeCode('H', *pos)


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
        """Clear the screen."""
        AnsiEscapeCode('J', 3).execute()
