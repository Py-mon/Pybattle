from pybattle.window.frames.frame import Frame, Borders
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size
from pybattle.ansi.colors import Colors
from pybattle.window.grid.range import RectRange

frame = Frame(Size(10, 20))
frame.add_frame(Frame(Size(3, 5)), Coord(2, 10))

frame.add_frame(Frame(Size(3, 5)), Coord(3, 8))

print(frame)