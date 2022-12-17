from pybattle.ansi.screen import Screen
from pybattle.window.frame import Frame

Screen.clear()

text = '''
KITTY CATS
EAT CHICKENS'''
  
window = Frame(text, (6, 15))
window.add_frame(Frame(size=(2, 5)))
