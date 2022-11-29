from colorama import Fore


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

# class