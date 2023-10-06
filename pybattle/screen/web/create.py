from pybattle.screen.web.element import Element, window

from pybattle.screen.frames.frame import Frame, Title
from pybattle.screen.grid.point import Coord, Size
from pybattle.screen.grid.cell import Cell
from pybattle.screen.frames.map import Map
from pybattle.screen.frames.weather import Weather, Rain
from pybattle.screen.colors import Colors


m1 = """
╭─ BEDROOM ─┬──────────────────╮
│   ╰───────╯       ||||       │
│                   ||||       │
│                     ─┬─┬─┬─┬─┤
│                              │
│                              │
│╭│╮   ╶─╮                     │
││││    ░│                     │
│╰│╯   ╶─╯           ╭─────┬─╮ │
│                    │░░░░░│▓│ │
│                    ╰─────┴─╯ │
╰──────────────────────────────╯
"""

m2 = Map(Cell.from_str(m1), Coord(7, 22))
m2[Coord(0, 0)].color = Colors.RED


weather = Weather(particles=["|"])


def update_weather():
    m2._update_weather(weather)


def update_player():
    m2._update_player()


def update():
    txt = ""
    for row in m2.rows:
        for cell in row:
            txt += f'<code style="color: rgb{cell.color.rgb};">{cell.value}</code>'

        # txt += "<br>"
    

    Element("text").edit(txt)
