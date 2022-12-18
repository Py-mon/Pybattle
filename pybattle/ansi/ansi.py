from enum import Enum


class CursorCode(Enum):
    """Codes for moving the cursor."""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    MOVE = 4


class AnsiEscSeq:
    """
    ANSI escape sequences are a standard for in-band signaling to control cursor location, color, font styling, and other options on terminals. 

    All ANSI escape sequences have a prefix; ESC (Escape).
    - Octal: \\033
    - Unicode: \\u001b
    - Hexadecimal: \\x1B (\\x1b)
    - Decimal: 27 (Note: This one does not work)

    The most useful sequences start with CSI (Control Sequence Introducer)
    - ESC[

    For example to make the color red: ESC[31m (\\033[31m) (Any ESC will work)

    Learn more here: https://en.wikipedia.org/wiki/ANSI_escape_code"""
    ESC = '\033'
    CSI = ESC + '['

    def __init__(self, code: CursorCode | str, *args: str | int) -> None:
        self.__code = code
        self.__args = args

    @property
    def __escape_code(self) -> str:
        """Returns the escape code based on the escape code type. If string, returns it."""
        if isinstance(self.__code, str):
            return self.__code

        match self.__code:
            case CursorCode.UP:
                return 'A'
            case CursorCode.DOWN:
                return 'B'
            case CursorCode.LEFT:
                return 'C'
            case CursorCode.RIGHT:
                return 'D'
            case CursorCode.MOVE:
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
        print(self.code, end='')
