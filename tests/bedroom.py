from pybattle.window.frames.map_frame import MapFrame
from pybattle.window.frames.frame import Frame
from pybattle.window.frames.center_frame import CenteredFrame
from pybattle.ansi.colors import Color
from pybattle.window.matrix import Matrix



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
