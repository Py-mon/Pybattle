from pybattle.window.frames.map_frame import MapFrame
from pybattle.window.frames.frame import Frame
from pybattle.ansi.colors import Colors
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size
from pybattle.window.frames.border.border_type import Borders


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
map_.add_frame(Frame(Size(2, 4)), Coord(1, 6))

print(map_)
