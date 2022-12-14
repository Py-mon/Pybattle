from enum import Enum
from typing import Tuple


class EscSeq(Enum):
    CURSOR_MOVE_UP = 0
    CURSOR_MOVE_DOWN = 1
    CURSOR_MOVE_LEFT = 2
    CURSOR_MOVE_RIGHT = 3
    MOVE_CURSOR = 4


class AnsiEscSeq:
    """
    ANSI escape sequences are a standard for in-band signaling to control cursor location, color, font styling, and other options on terminals. 
    
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
        self.__code = code
        self.__args = args

    @property
    def __escape_code(self) -> str:
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
    def __escape_args(self) -> str:
        """Returns the args of the escape sequence.
        >>> [12, 43] -> '12;43'
        """
        return "".join([str(arg) + ';' for arg in self.__args])[:-1]
    
    @property
    def code(self) -> str:
        return self.CSI + self.__escape_args + self.__escape_code

    def execute(self) -> None:
        """Execute the ANSI escape code."""
        print(self.__code, end='')
