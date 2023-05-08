from copy import copy
from typing import Iterator, Optional

from colorama import Fore

from pybattle.ansi.ansi import AnsiEscSeq


class ColorType:
    """A 4-bit color ANSI escape code"""

    def __init__(self, color_code: AnsiEscSeq, name: Optional[str] = None) -> None:
        self.__color_code = color_code
        if name is None:
            self.name = "N/A"
        else:
            self.name = name

    def __iter__(self) -> Iterator[str]:
        return iter(self.__color_code.code)

    def __str__(self) -> str:
        return self.__color_code.code

    def use(self) -> None:
        self.__color_code.exec()


class Colors:
    """Stores all 4-bit ANSI escape code colors"""
    
    DEFAULT = ColorType(AnsiEscSeq(Fore.RESET), "DEFAULT")  #  VSCODE
    BLACK = ColorType(AnsiEscSeq(Fore.BLACK), "BLACK")  # 0x000000
    GRAY = ColorType(AnsiEscSeq(Fore.LIGHTBLACK_EX), "GRAY")  # 0x666666
    BRIGHT_WHITE = ColorType(AnsiEscSeq(Fore.LIGHTWHITE_EX), "BRIGHT_WHITE")  # 0xE5E5E5
    BRIGHT_RED = ColorType(AnsiEscSeq(Fore.LIGHTRED_EX), "BRIGHT_RED")  # 0xF14C4C
    RED = ColorType(AnsiEscSeq(Fore.RED), "RED")  # 0xCD3131
    YELLOW = ColorType(AnsiEscSeq(Fore.YELLOW), "YELLOW")  # 0xE5E510
    BRIGHT_YELLOW = ColorType(
        AnsiEscSeq(Fore.LIGHTYELLOW_EX), "BRIGHT_YELLOW"
    )  # 0xF5F543
    BRIGHT_GREEN = ColorType(AnsiEscSeq(Fore.LIGHTGREEN_EX), "BRIGHT_GREEN")  # 0x23D18B
    GREEN = ColorType(AnsiEscSeq(Fore.GREEN), "GREEN")  # 0x0DBC79
    CYAN = ColorType(AnsiEscSeq(Fore.CYAN), "CYAN")  # 0x11A8CD
    BRIGHT_CYAN = ColorType(AnsiEscSeq(Fore.LIGHTCYAN_EX), "BRIGHT_CYAN")  # 0x29B8DB
    BRIGHT_BLUE = ColorType(AnsiEscSeq(Fore.LIGHTBLUE_EX), "BRIGHT_BLUE")  # 0x3B8EEA
    BLUE = ColorType(AnsiEscSeq(Fore.BLUE), "BLUE")  # 0x2472C8
    MAGENTA = ColorType(AnsiEscSeq(Fore.MAGENTA), "MAGENTA")  # 0xBC3FBC
    BRIGHT_MAGENTA = ColorType(
        AnsiEscSeq(Fore.LIGHTMAGENTA_EX), "BRIGHT_MAGENTA"
    )  # 0xD670D6


def next_color(self, coord, coords):
    """Lexicographically find the next coord where a color is. Returns None if there are none beyond it.

    Now unused but still here because it is beautiful"""
    # If there are no colors then there are no more colors beyond it
    if len(coords) == 0:
        return None

    if coord not in coords:
        coords.append(coord)

    coords.sort()

    if coord == coords[-1]:
        return None

    index = coords.index(coord) + 1

    coord = copy(coords[index])
    coord.x -= 1

    return coord
