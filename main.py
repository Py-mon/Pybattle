from pybattle.ansi.screen import Screen
from pybattle.window.frame import Frame
from pybattle.ansi.color import Colors
from pybattle.window.matrix import Matrix, ColorCoord
from pybattle.window.window import Window

Screen.clear()

# text = '''
# KITTY CATS
# EAT CHICKENS'''
  
# window0 = Frame(text, (6, 15))
# window0.add_frame(Frame(size=(2, 5)))

window1 = Window(Frame(size=(5, 5)))
window2 = Window(Frame(size=(4, 4)))
window3 = Window(Frame(size=(6, 6)))

window1.set()
window2.set()
window3.set()

Window.show()
