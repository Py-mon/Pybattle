from time import sleep

from window.frames.frame import Frame

from pybattle.ansi.colors import Colors
from pybattle.window.frames.border.border_type import Borders
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size

map_ = Frame.map(
    """
                   ||||       
                   ||||       
                     ─┬─┬─┬─┬─
                              
                              
╭│╮   ╶─╮                     
│││    ░│                     
╰│╯   ╶─╯           ╭─────┬─╮ 
                    │░░░░░│▓│ 
                    ╰─────┴─╯ 
""",
    "BEDROOM",
    border_color=Colors.RED,
    title_color=Colors.BLUE,
)

map_.add_frame(Frame.box(Size(2, 9)), Coord(0, 4))
map_.add_frame(Frame.box(Size(2, 4)), Coord(1, 6))

map_.update()

print(map_)


print(Frame.centered("Play\nSettings\nQuit", Size(9, 19)))


sleep(5)
