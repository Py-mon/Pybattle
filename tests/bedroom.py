from pybattle.window.frames.map_frame import MapFrame
from pybattle.window.frames.frame import Frame


map_ = MapFrame('''
                   ||||       
                   ||||       
                     ─┬─┬─┬─┬─
                              
                              
╭│╮   ╶─╮                     
│││    ░│                     
╰│╯   ╶─╯           ╭─────┬─╮ 
                    │░░░░░│▓│ 
                    ╰─────┴─╯ 
''', title='BEDROOM')

map_.add_frame(Frame((2, 9)), (0, 4))
