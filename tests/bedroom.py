from pybattle.window.frames.map_frame import MapFrame
from pybattle.window.frames.frame import Frame
from pybattle.ansi.colors import Colors
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size


map_ = MapFrame('''
                   ||||       
                   ||||       
                     ─┬─┬─┬─┬─
                              
                              
╭│╮   ╶─╮                     
│││    ░│                     
╰│╯   ╶─╯           ╭─────┬─╮ 
                    │░░░░░│▓│ 
                    ╰─────┴─╯ 
''', 'BEDROOM', Colors.RED, Colors.BLUE)

map_.add_frame(Frame(Size(2, 9)), Coord(0, 4))

print(map_)
