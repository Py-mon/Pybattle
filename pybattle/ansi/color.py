from typing import Iterator, Optional

from colorama import Fore

from pybattle.ansi.ansi import AnsiEscSeq


class Color:
    """A 4-bit color ANSI escape code."""
    
    def __init__(self, color_code: AnsiEscSeq, name: Optional[str] = None) -> None:
        self.__color_code = color_code
        if name is None:
            self.name = 'N/A'
        else:
            self.name = name

    def __iter__(self) -> Iterator[str]:
        return iter(self.__color_code.code)

    def __str__(self) -> str:
        return self.__color_code.code
    
    def use(self) -> None:
        self.__color_code.execute()


class Colors:
    DEFAULT = Color(AnsiEscSeq(Fore.RESET), 'DEFAULT')                          #  VSCODE
    BLACK = Color(AnsiEscSeq(Fore.BLACK), 'BLACK')                              # 0x000000
    GRAY = Color(AnsiEscSeq(Fore.LIGHTBLACK_EX), 'GRAY')                        # 0x666666
    BRIGHT_WHITE = Color(AnsiEscSeq(Fore.LIGHTWHITE_EX), 'BRIGHT_WHITE')        # 0xE5E5E5
    BRIGHT_RED = Color(AnsiEscSeq(Fore.LIGHTRED_EX), 'BRIGHT_RED')              # 0xF14C4C
    RED = Color(AnsiEscSeq(Fore.RED), 'RED')                                    # 0xCD3131
    YELLOW = Color(AnsiEscSeq(Fore.YELLOW), 'YELLOW')                           # 0xE5E510
    BRIGHT_YELLOW = Color(AnsiEscSeq(Fore.LIGHTYELLOW_EX), 'BRIGHT_YELLOW')     # 0xF5F543
    BRIGHT_GREEN = Color(AnsiEscSeq(Fore.LIGHTGREEN_EX), 'BRIGHT_GREEN')        # 0x23D18B
    GREEN = Color(AnsiEscSeq(Fore.GREEN), 'GREEN')                              # 0x0DBC79
    CYAN = Color(AnsiEscSeq(Fore.CYAN), 'CYAN')                                 # 0x11A8CD
    BRIGHT_CYAN = Color(AnsiEscSeq(Fore.LIGHTCYAN_EX), 'BRIGHT_CYAN')           # 0x29B8DB
    BRIGHT_BLUE = Color(AnsiEscSeq(Fore.LIGHTBLUE_EX), 'BRIGHT_BLUE')           # 0x3B8EEA
    BLUE = Color(AnsiEscSeq(Fore.BLUE), 'BLUE')                                 # 0x2472C8
    MAGENTA = Color(AnsiEscSeq(Fore.MAGENTA), 'MAGENTA')                        # 0xBC3FBC
    BRIGHT_MAGENTA = Color(AnsiEscSeq(Fore.LIGHTMAGENTA_EX), 'BRIGHT_MAGENTA')  # 0xD670D6
