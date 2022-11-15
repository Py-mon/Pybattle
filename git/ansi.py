from os import system
from time import sleep

from colorama import Fore

ESC = '\033'
CSI = ESC + '['


def execute_CSI_code(code: str | int, *args: str | int):
    print(CSI + "".join([str(arg) + ';' for arg in args]
          [:-1]) + str(code), end='')


def set_title(title: str):
    system(f'title {title}')


class _Color:
    NORMAL = Fore.RESET
    DEFAULT = NORMAL
    RESET = NORMAL
    BLACK = Fore.BLACK                     # #000000
    GRAY = Fore.LIGHTBLACK_EX              # #666666
    BRIGHT_WHITE = Fore.LIGHTWHITE_EX      # #E5E5E5

    BRIGHT_RED = Fore.LIGHTRED_EX          # #F14C4C
    RED = Fore.RED                         # #CD3131
    YELLOW = Fore.YELLOW                   # #E5E510
    BRIGHT_YELLOW = Fore.LIGHTYELLOW_EX    # #F5F543
    BRIGHT_GREEN = Fore.LIGHTGREEN_EX      # #23D18B
    GREEN = Fore.GREEN                     # #0DBC79
    CYAN = Fore.CYAN                       # #11A8CD
    BRIGHT_CYAN = Fore.LIGHTCYAN_EX        # #29B8DB
    BRIGHT_BLUE = Fore.LIGHTBLUE_EX        # #3B8EEA
    BLUE = Fore.BLUE                       # #2472C8
    MAGENTA = Fore.MAGENTA                 # #BC3FBC
    BRIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX  # #D670D6


class _Cursor:
    def __init__(self) -> None:
        self.pos = (0, 0)

    def up(cls, n: int = 1) -> None:
        """Moves the cursor `n` cells up."""
        cls.pos = cls.pos[0] - 1, cls.pos[1]
        execute_CSI_code('A', n)

    def down(cls, n: int = 1) -> None:
        """Moves the cursor `n` cells down."""
        cls.pos = cls.pos[0] + 1, cls.pos[1]
        execute_CSI_code('B', n)

    def forward(cls, n: int = 1) -> None:
        """Moves the cursor `n` cells forward (right)."""
        cls.pos = cls.pos[0], cls.pos[1] + 1
        execute_CSI_code('C', n)

    def back(cls, n: int = 1) -> None:
        """Moves the cursor `n` cells back (left)."""
        cls.pos = cls.pos[0], cls.pos[1] - 1
        execute_CSI_code('D', n)

    def move(cls, pos: tuple[int, int]) -> None:
        cls.pos = pos
        execute_CSI_code('H', *pos)


Color = _Color()
Cursor = _Cursor()


class _Screen:
    def __init__(self, cursor: _Cursor) -> None:
        self.__cursor = cursor
        self.clear(3)

    def clear_line(mode: int | str = 2):
        execute_CSI_code('K', mode)

    def clear(self, mode: int | str = 2):
        self.__cursor.pos = (0, 0)
        execute_CSI_code('J', mode)

    def write(self, txt: str, pos: tuple[int, int] = ..., color: _Color = Color.DEFAULT, move_cursor: bool = True) -> None:
        if pos is not ...:
            self.move(pos)
        else:
            height = txt.count('\n')
            width = len(max(txt.split('\n')))
            self.__cursor.pos = self.__cursor.pos[0] + height, self.__cursor.pos[1] + width

        if color is not None:
            print(color, end='')
        print(txt, end='')

        if not move_cursor:
            self.back(txt.count('\n'))


Screen = _Screen(Cursor)

Screen.write('hi\nthere')
Screen.write(str(Cursor.pos))
