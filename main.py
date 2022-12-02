from src.window.code import str_with_text
from src.window.color import Color
from src.window.screen import Screen
from src.window.code import Code

Screen.clear()


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
''', Code((2, 2), Color.RED), Code((4, 2), Color.DEFAULT))

print(test_str)

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
