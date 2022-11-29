# map = Window('''\
#                    ||||
#                    ||||
#                      ─┬─┬─┬─┬─


# ╭│╮   ╶─╮
# │││    ░│
# ╰│╯   ╶─╯           ╭─────┬─╮
#                     │░░░░░│▓│
#                     ╰─────┴─╯
# ''', name='BEDROOM')

# map.add_frame(Frame(size=(2, 9)), (4, 0))

from os import system

from src.window.color import Color
from src.window.matrix import Matrix
from src.window.screen import Screen

Screen.clear()  # doesn't work


system('cls')


test_str = Matrix(f'''
╭───────────╮
│╭─╮        │
││{Color.RED}a{Color.DEFAULT}│        │
│╰─╯        │
│   ╭─╮     │
│   │b│     │
│   ╰─╯     │
│           │
│           │
│        ╭─╮│
│        │c││
│        ╰─╯│
╰───────────╯
''')

print(test_str)
