from src.window.code import str_with_text
from src.window.color import Color
from src.window.screen import Screen
from src.window.code import Code
from src.window.frame import Window, Frame

Screen.clear()


# test_str = str_with_text('''\
# ╭───────────╮
# │╭─╮        │
# ││a│        │
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
# ''', Code((2, 2), Color.MAGENTA))

# print(test_str)

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

map = Window(size=(20, 20), name='HI')

map.add_frame(Window(size=(2, 9)), (0, 20))
