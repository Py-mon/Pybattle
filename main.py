from os import system
from time import sleep
import re

from src.window.frame import Frame, Window
from src.window.color import Color
from src.window.matrix import Matrix

system('clear') # Change to "clear" if you are not on windows

main = Window((40, 60))
main.add_frame(Frame((6, 20)), (3, 3))
main.add_frame(Frame((2, 2)))

test_str = Matrix(f'''
╭───────────╮
│╭─╮        │
││{Color.RED}d{Color.DEFAULT}│        │
│╰─╯        │
│   ╭─╮     │
│   │{Color.BLUE}b{Color.DEFAULT}│     │
│   ╰─╯     │
│   {Color.GREEN}f{Color.DEFAULT}       │
│           │
│        ╭─╮│
│        │{Color.MAGENTA}c{Color.DEFAULT}││
│        ╰─╯│
╰───────────╯
''')

print(test_str)

# print(test_str)
# test_str = f'{Color.RED} Hello world, {Color.BLUE} This is {Color.DEFAULT}'
# print(test_str)
# print(remove_and_save_escape_chars(test_str))