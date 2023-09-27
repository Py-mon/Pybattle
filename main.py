from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.frame import Frame
from pybattle.screen.frames.map import Map
from pybattle.screen.frames.menu import Menu, Selection, SwitchSelection, VoidSelection
from pybattle.screen.frames.weather import Rain, Weather
from pybattle.screen.grid.matrix import Cell, Grid
from pybattle.screen.grid.point import Coord, Size
from pybattle.screen.window import Event, EventExit, EventQueue, Window, keys_pressing
from pybattle.types_ import CardinalDirection
from pybattle.creatures.attributes.move import Move
from pybattle.creatures.attributes.element import Element

# r"""
#    _-----_
#    | , , |
#    |  -  |
#   __|---|__
#  / |     | \
#  \ |_____| /
#   ^| | | |^
#    | | | |
#    |_| |_|

# """
# x = r"""
#    _-----_
#    ┃ , , ┃
#    ┃  -  ┃
#   __┃───┃__
#  / ┃     ┃ \
#  \ ┃_____┃ /
#   ^┃ ┃ ┃ ┃^
#    ┃ ┃ ┃ ┃
#    ┃_┃ ┃_┃
# """

# w = Window(Matrix(Cell.from_str(x)))
# w.run()


# f = Frame(Cell.from_size(Size(15, 40)))
# m1 = """
# ╭─ BEDROOM ─┬──────────────────╮
# │   ╰───────╯       ||||       │
# │                   ||||       │
# │                     ─┬─┬─┬─┬─┤
# │                              │
# │                              │
# │╭│╮   ╶─╮                     │
# ││││    ░│                     │
# │╰│╯   ╶─╯           ╭─────┬─╮ │
# │                    │░░░░░│▓│ │
# │                    ╰─────┴─╯ │
# ╰──────────────────────────────╯
# """


# m2 = Map(Cell.from_str(m1), Coord(7, 22))
# m2[Coord(5, 5)].value = "^"
# m2[Coord(5, 5)].collision = False

# f.add_frame(m2.camera())
# print(f)


# w = Window(f)

# w.one_time_event(lambda: Rain(CardinalDirection.EAST, frequency=0.17), 3)


# def update1():
#     f.add_frame(m2.camera())
#     w.change(f)

#     # if m2[m2.pos].value == "^":
#     #     w.extend_current_events(Event(lambda: EventExit.QUIT, 0.01), 3)


# e1 = Event(update1, 0.01)


# m2.events.append(e1)


# w.run(EventQueue(m2.events))


# ╭─ Wind Bash ─ Air ─╮ ╭─ Slash ── Normal ─╮
# │ 50 STR    90% ACC │ │ 35 STR      20 EC │
# │ Physical    25 EC │ ╰───────────────────╯
# ╰───────────────────╯
# ╭─ Dodge ───────────╮ ╭─ Tornado ─── Air ─╮
# │ Support     30 EC │ │ 70 STR      50 EC │
# ╰───────────────────╯ ╰───────────────────╯

move1 = Move(
    "Wind Bash",
    Element("Air", {}),
    None,
    energy_cost=25,
    strength=50,
    type_="Physical",
    accuracy=90,
)

move2 = Move(
    "Slash",
    Element("Normal", {}),
    None,
    energy_cost=20,
    strength=35,
    type_="Physical",
    accuracy=99,
)

move3 = Move(
    "Dodge",
    Element("Normal", {}),
    None,
    energy_cost=0,
    type_="Support",
    accuracy=80,
)

move4 = Move(
    "Dodge",
    Element("Air", {}),
    None,
    energy_cost=50,
    strength=70,
    type_="Magical",
    accuracy=95,
)


m = Menu(
    Cell.from_size(Size(7, 50)),
    [
        SwitchSelection(
            Selection(
                str(move1.frame),
                Coord(1, 2),
            ),
            Selection(
                str(move1.bottom_extended_frame),
                Coord(1, 2),
            ),
        ),
        SwitchSelection(
            Selection(
                str(move2.frame),
                Coord(1, 24),
            ),
            Selection(
                str(move2.bottom_extended_frame),
                Coord(1, 24),
            ),
        ),
        SwitchSelection(
            Selection(
                "\n\n" + str(move3.frame),
                Coord(4, 2),
            ),
            Selection(
                str(move3.top_extended_frame),
                Coord(4, 2),
            ),
        ),
        SwitchSelection(
            Selection(
                "\n\n" + str(move4.frame),
                Coord(4, 24),
            ),
            Selection(
                str(move4.top_extended_frame),
                Coord(4, 24),
            ),
        ),
    ],
)

w = Window(m)


def update():
    w.change(m)
    return m.switch()


e1 = Event(update, 0.05)

w.run(EventQueue([e1]))


# m = Menu(
#     Cell.from_size(Size(15, 40)),
#     [
#         SwitchSelection(
#             Selection("Start\nOver", Coord(2, 2), Colors.DEFAULT),
#             Selection("Start\nOver", Coord(2, 2), Colors.BLUE),
#         ),
#         SwitchSelection(
#             Selection("Settings", Coord(4, 6), Colors.DEFAULT),
#             Selection("Settings", Coord(4, 6), Colors.GRAY),
#         ),
#         SwitchSelection(
#             Selection("Quit", Coord(6, 2), Colors.DEFAULT),
#             Selection("Quit", Coord(6, 2), Colors.RED),
#         ),
#     ],
# )
# m2 = Menu.centered_list(
#     Cell.from_size(Size(15, 40)),
#     [
#         SwitchSelection(
#             VoidSelection("Continue", Colors.DEFAULT),
#             VoidSelection("Continue", Colors.CYAN),
#         ),
#         SwitchSelection(
#             VoidSelection("Settings", Colors.DEFAULT),
#             VoidSelection("Settings", Colors.GRAY),
#         ),
#         SwitchSelection(
#             VoidSelection("Quit", Colors.DEFAULT),
#             VoidSelection("Quit", Colors.RED),
#         ),
#     ],
# )
# #
# w = Window(m)


# def update(_):
#     w.change(m)
#     return m.switch()


# e1 = Event(update, 0.05)


# def update1(_):
#     print("hi")
#     if "BackSpace" in keys_pressing:
#         return (EventExit.BREAK_QUEUE, "Not Settings")
# def update1(_):
#     print("hi")
#     if "BackSpace" in keys_pressing:
#         return EventExit.QUIT


# e11 = Event(update1, 0.5)


# def update2(last):
#     if last["update"].label != "Settings":
#         return EventExit.BREAK

#     result = m2.switch()
#     if result is not None:
#         print("HERE", result.label)
#         w.extend_event_queue([e1])
#         return EventExit.BREAK
#     w.change(m2)


# e2 = Event(update2, 0.05)


# w.run(EventQueue([e1], [e2]))


# def update2(m, ma):
#     result = m.switch()
#     if result is not None:
#         Event(update, 0.05, ma)
#         return True
#     w.change(m)


# def update(m):
#     result = m.switch()
#     if result is not None:
#         # return result # TODO or logic here
#         m2 = Menu(
#             Cell.from_size(Size(15, 40)),
#             [
#                 SwitchSelection(
#                     Selection(result.label, Coord(2, 2), Colors.DEFAULT),
#                     Selection(result.label, Coord(2, 2), Colors.CYAN),
#                 ),
#                 SwitchSelection(
#                     Selection("Back", Coord(4, 2), Colors.DEFAULT),
#                     Selection("Back", Coord(4, 2), Colors.CYAN),
#                 ),
#             ],
#         )
#         Event(update2, 0.05, m2, m)
#         return True
#     w.change(m)
