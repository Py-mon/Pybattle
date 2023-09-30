from pybattle.screen.frames.frame import Frame, Title
from pybattle.screen.grid.point import Coord, Size
from pybattle.screen.grid.cell import Cell
from pybattle.screen.frames.map import Map
from pybattle.screen.frames.weather import Weather, Rain


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


weather = Weather(particles=["."])

while True:
    m2._update_weather(weather)
    document.getElementById("text").innerHTML = str(m2).replace("\n", "<br>")
