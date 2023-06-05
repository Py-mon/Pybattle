"""Includes all the 4-bit colors."""

from typing import Optional

from colorama import Fore

from pybattle.ansi.ansi import AnsiEscSeq


class ColorType:
    """A 4-bit color ANSI escape code"""

    def __init__(self, seq: AnsiEscSeq, color_name: Optional[str] = None) -> None:
        self.seq = seq
        self.color_name = color_name

    def __repr__(self) -> str:
        return str(self.color_name)

    def apply(self) -> None:
        """Apply the color to the terminal"""
        self.seq.exec()


class Colors:
    """Provides all the 4-bit ANSI escape sequence colors"""

    DEFAULT = ColorType(AnsiEscSeq(Fore.RESET), "DEFAULT")  # HEX CODE
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
