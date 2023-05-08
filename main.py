from time import sleep

from pybattle.ansi.colors import Colors
from pybattle.ansi.screen import Screen
from pybattle.window.event import Event
from pybattle.window.frames.frame import Frame
from pybattle.window.frames.menu import (
    FrameSelection,
    Menu,
    Selection,
    SwitchSelection,
    VoidSelection,
)
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size

m = Menu(
    Frame.box(Size(5, 24)),
    [
        SwitchSelection(
            Selection("Attack", Coord(1, 1), Colors.RED),
            FrameSelection(Frame.map("Attack", base_color=Colors.RED), Coord(1, 1)),
        ),
        SwitchSelection(
            Selection("Items", Coord(1, 9), Colors.GRAY),
            FrameSelection(Frame.map("Items", base_color=Colors.GRAY), Coord(1, 9)),
        ),
        SwitchSelection(
            Selection("Flee", Coord(1, 16), Colors.MAGENTA),
            FrameSelection(Frame.map("Flee", base_color=Colors.MAGENTA), Coord(1, 16)),
        ),
    ],
)

# m = Menu.centered_list(
#     Frame.box(Size(9, 16)),
#     [
#         SwitchSelection(
#             VoidSelection("Attack", Colors.DEFAULT),
#             VoidSelection("Attack", Colors.RED),
#         ),
#         SwitchSelection(
#             VoidSelection("Items", Colors.DEFAULT),
#             VoidSelection("Items", Colors.GRAY),
#         ),
#         SwitchSelection(
#             VoidSelection("Flee", Colors.DEFAULT),
#             VoidSelection("Flee", Colors.MAGENTA),
#         ),
#     ],
# )


def write():
    sleep(0.1)
    Screen.write(m.frame)


Event(m.event, stop_all=True)
Event(write)


Event.start_all()


print(Event.get_next_result())
