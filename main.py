# from src.window.code import str_with_text
# from src.window.color import Color
# from src.window.code import Code
# from src.window.frame import Window, Frame

from src.window.screen import Screen

Screen.clear()

import src.matrix.matrix


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

# map_ = Window('CENTERED', (11, 21))

# print(map_.matrix)
