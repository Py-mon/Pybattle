from typing import Optional

from colorama import Fore

from src.window.screen import AnsiEscapeCode


class Color:
    """A 4-bit color ANSI escape code."""
    def __init__(self, color_code: AnsiEscapeCode, name: Optional[str] = None) -> None:
        self._color_code = color_code.code
        if name is None:
            self.name = 'N/A'
        else:
            self.name = name
    
    @classmethod
    def init_colors(cls) -> None:
        cls.DEFAULT = Color(AnsiEscapeCode(Fore.RESET), 'DEFAULT')

        cls.BLACK = Color(AnsiEscapeCode(Fore.BLACK), 'BLACK')                              # 0x000000
        cls.GRAY = Color(AnsiEscapeCode(Fore.LIGHTBLACK_EX), 'GRAY')                        # 0x666666
        cls.BRIGHT_WHITE = Color(AnsiEscapeCode(Fore.LIGHTWHITE_EX), 'BRIGHT_WHITE')        # 0xE5E5E5
  
        cls.BRIGHT_RED = Color(AnsiEscapeCode(Fore.LIGHTRED_EX), 'BRIGHT_RED')              # 0xF14C4C
        cls.RED = Color(AnsiEscapeCode(Fore.RED), 'RED')                                    # 0xCD3131
        cls.YELLOW = Color(AnsiEscapeCode(Fore.YELLOW), 'YELLOW')                           # 0xE5E510
        cls.BRIGHT_YELLOW = Color(AnsiEscapeCode(Fore.LIGHTYELLOW_EX), 'BRIGHT_YELLOW')     # 0xF5F543
        cls.BRIGHT_GREEN = Color(AnsiEscapeCode(Fore.LIGHTGREEN_EX), 'BRIGHT_GREEN')        # 0x23D18B
        cls.GREEN = Color(AnsiEscapeCode(Fore.GREEN), 'GREEN')                              # 0x0DBC79
        cls.CYAN = Color(AnsiEscapeCode(Fore.CYAN), 'CYAN')                                 # 0x11A8CD
        cls.BRIGHT_CYAN = Color(AnsiEscapeCode(Fore.LIGHTCYAN_EX), 'BRIGHT_CYAN')           # 0x29B8DB
        cls.BRIGHT_BLUE = Color(AnsiEscapeCode(Fore.LIGHTBLUE_EX), 'BRIGHT_BLUE')           # 0x3B8EEA
        cls.BLUE = Color(AnsiEscapeCode(Fore.BLUE), 'BLUE')                                 # 0x2472C8
        cls.MAGENTA = Color(AnsiEscapeCode(Fore.MAGENTA), 'MAGENTA')                        # 0xBC3FBC
        cls.BRIGHT_MAGENTA = Color(AnsiEscapeCode(Fore.LIGHTMAGENTA_EX), 'BRIGHT_MAGENTA')  # 0xD670D6
        
    def __iter__(self):
        return iter(self._color_code)
    
    def __str__(self) -> str:
        return self._color_code
    
    def __repr__(self) -> str:
        return f'Color({self.name})'


Color.init_colors()
