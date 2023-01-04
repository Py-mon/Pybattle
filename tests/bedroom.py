from pybattle.window.frames.map_frame import MapFrame
from pybattle.window.frames.frame import Frame
from pybattle.ansi.colors import Color


map_ = MapFrame('''
                   ||||       
                   ||||       
                     ─┬─┬─┬─┬─
                              
                              
╭│╮   ╶─╮                     
│││    ░│                     
╰│╯   ╶─╯           ╭─────┬─╮ 
                    │░░░░░│▓│ 
                    ╰─────┴─╯ 
''', 'BEDROOM', Color.RED, Color.BLUE)

map_.add_frame(Frame((2, 9)), (0, 4))

print(map_)
