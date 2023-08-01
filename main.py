from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.frame import Frame
from pybattle.screen.frames.menu2 import Menu, Selection, SwitchSelection
from pybattle.screen.grid.matrix import Cell, Matrix
from pybattle.screen.grid.point import Coord, Size
from pybattle.screen.window import Event, Window

m = Menu(
    Cell.from_size(Size(15, 40)),
    [
        SwitchSelection(
            Selection("Start\nOver", Coord(2, 2), Colors.DEFAULT),
            Selection("Start\nOver", Coord(2, 2), Colors.CYAN),
        ),
        SwitchSelection(
            Selection("Settings", Coord(4, 2), Colors.DEFAULT),
            Selection("Settings", Coord(4, 2), Colors.CYAN),
        ),
        SwitchSelection(
            Selection("Quit", Coord(6, 2), Colors.DEFAULT),
            Selection("Quit", Coord(6, 2), Colors.CYAN),
        ),
    ],
)

w = Window(m)


def update():
    m.switch()
    w.change(m)


Event(update, 0.05)

w.run()
