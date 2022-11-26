from os import system
from time import sleep

from src.window.frame import Frame, Window

system('cls') # Change to "clear" if you are not on windows


map = Window('''\
                   ||||       
                   ||||       
                     ─┬─┬─┬─┬─
                              
                              
╭│╮   ╶─╮                     
│││    ░│                     
╰│╯   ╶─╯           ╭─────┬─╮ 
                    │░░░░░│▓│ 
                    ╰─────┴─╯ 
''')

map.add_frame(Frame(size=(2, 9)), (4, 0))
