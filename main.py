from pybattle.ansi.screen import Screen
from pybattle.window.frame import Frame
from pybattle.ansi.color import Colors
from pybattle.window.matrix import Matrix, ColorCoord
Screen.clear()

# text = '''
# KITTY CATS
# EAT CHICKENS'''
  
# window = Frame(text, (6, 15))
# window.add_frame(Frame(size=(2, 5)))


from pybattle.ansi.input import SelectionMenu, Selection


SelectionMenu((15, 15), [Selection('a', (1, 1)), Selection('b', (4, 4)), Selection('c', (8, 8))])
# x = Matrix('hello', ColorCoord(0, Colors.GRAY))
# print(x)
# y = Frame(x)
# print(y.matrix)
