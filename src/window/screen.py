from typing import Optional

from colorama import Fore

from src.types_ import CoordReference
from src.window.coord import Coord


class AnsiEscapeCode:
    """https://en.wikipedia.org/wiki/ANSI_escape_code"""
    ESC = '\033'
    CSI = ESC + '['

    def __init__(self, code: str, *args: str | int) -> None:
        self.code = self.CSI + \
            "".join([str(arg) + ';' for arg in args])[:-1] + code

    def execute(self) -> None:
        """Execute the ANSI escape code."""
        print(self.code, end='')


class Color:
    NORMAL = Fore.RESET
    DEFAULT = NORMAL
    RESET = NORMAL

    BLACK = Fore.BLACK                     # 0x000000
    GRAY = Fore.LIGHTBLACK_EX              # 0x666666
    BRIGHT_WHITE = Fore.LIGHTWHITE_EX      # 0xE5E5E5

    BRIGHT_RED = Fore.LIGHTRED_EX          # 0xF14C4C
    RED = Fore.RED                         # 0xCD3131
    YELLOW = Fore.YELLOW                   # 0xE5E510
    BRIGHT_YELLOW = Fore.LIGHTYELLOW_EX    # 0xF5F543
    BRIGHT_GREEN = Fore.LIGHTGREEN_EX      # 0x23D18B
    GREEN = Fore.GREEN                     # 0x0DBC79
    CYAN = Fore.CYAN                       # 0x11A8CD
    BRIGHT_CYAN = Fore.LIGHTCYAN_EX        # 0x29B8DB
    BRIGHT_BLUE = Fore.LIGHTBLUE_EX        # 0x3B8EEA
    BLUE = Fore.BLUE                       # 0x2472C8
    MAGENTA = Fore.MAGENTA                 # 0xBC3FBC
    BRIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX  # 0xD670D6


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
        if isinstance(pos, tuple):
            pos = Coord(*pos)

        txt = str(txt)

        if pos is not ...:
            Cursor.move(pos).execute()

        if color is not None:
            print(color, end='')
            
        for line in txt.splitlines():
            Cursor.left(Cursor.pos.x).execute()
            print(line)

        Cursor.pos.x += txt.count('\n')
        Cursor.pos.y += len(max(txt.split('\n')))

        if not move_cursor:
            Cursor.up(txt.count('\n')).execute()
