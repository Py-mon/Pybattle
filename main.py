# from src.window.code import str_with_text
# from src.window.color import Color
# from src.window.code import Code
from pybattle.matrix.frame import Window

from pybattle.window.screen import Screen

Screen.clear()

from pybattle.matrix.matrix import Matrix, ColorCoord, Colors

# array = Matrix(
# f'''
# 1230
# 4560
# 7890
# ''', ColorCoord((0, 0), Colors.MAGENTA), ColorCoord((2, 0), Colors.RED), ColorCoord((3, 0), Colors.BLUE))

# print(repr(array))
# print(str(array))
# print(array.size)

# print(array[(0, 0):(1, 2)])
# array[(0, 0):(1, 2)] = Matrix(
# f'''
# 99
# 99
# 99
# ''')
# print(repr(array))

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

# map_ = Window('''
#                    ||||       
#                    ||||       
#                      ─┬─┬─┬─┬─
                              
                              
# ╭│╮   ╶─╮                     
# │││    ░│                     
# ╰│╯   ╶─╯           ╭─────┬─╮ 
#                     │░░░░░│▓│ 
#                     ╰─────┴─╯ 
# ''', name='HELLO')

# print(map_.size)

# map_.add_frame(Window(size=(5, 7)), (3, 0))


Window('CENTERED', (11, 11))

window = Window(size=(10, 10))

# print(window.size)
# print(window.inner_size)

# x = window.size.center - Matrix('\nAB\n').size

# window[x] = 'AB'

# print(repr(window.matrix))