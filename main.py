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
from src.window.code import str_with_text

Screen.clear()  # doesn't work


system('cls')

test_str = str_with_text('''\
╭───────────╮
│╭─╮        │
││a│        │
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
''', [2, Color.RED])

print(test_str)

test_str = Matrix(test_str)

# test_str = Matrix(f'''\
# ╭───────────╮
# │╭─╮        │
# ││{Color.RED}a{Color.DEFAULT}│        │
# │╰─╯        │
# │   ╭─╮     │
# │   │b│     │
# │   ╰─╯     │
# │           │
# │           │
# │        ╭─╮│
# │        │c││
# │        ╰─╯│
# ╰───────────╯
# ''')

print(test_str)
