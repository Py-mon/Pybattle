from copy import copy
from random import choices
from typing import Optional, Self

from pybattle.log.log import logger
from pybattle.types_ import CardinalDirection
from pybattle.window.event import Event, EventGroup, Scene
from pybattle.window.frames.border.border_type import Borders
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Cell, Junction, Matrix
from pybattle.window.grid.size import Size
from pybattle.window.input import Keyboard, key_listener
from pybattle.window.map.weather import Rain, Weather
from pybattle.window.screen.screen import Screen

Rain(CardinalDirection.WEST)


# TODO add maps to frames
# TODO maybe add characters to the map
class Map:
    def __init__(
        self,
        map_: Frame,
        starting_pos: Coord,
        exits: list[Coord] = [],
        player_char: str = "♀",  # 'º ⏺ ○ ● ◯ ☃ ☹ ☻ ☺ ♀ ♂ ⚬ ⚲ ⚴ ⛑ ⛹ ⫯ x X' 𓀞
    ):
        self.frame = map_
        self.frame.update()

        self.matrix = self.frame.contents

        self.exits: dict[Coord, tuple[Optional[Self], ellipsis | Coord]] = {}
        for exit in exits:
            self.exits[exit] = (None, ...)

        self.pos = starting_pos
        self.range_ = Size(3, 10)
        self.player_char = player_char

        self.closed: bool = True

        self.open_cells = []
        for coord in self.frame.contents.coords:
            cell = self.frame[coord]
            if not cell.collision and not isinstance(cell, Junction):
                self.open_cells.append(coord)

        self.scene = Scene(self.camera, Coord(5, 5))
        
        self.previous = copy(self.pos)

    def camera(self):
        end = self.pos + self.range_
        start = self.pos - self.range_

        if start.x == 0:
            end.x += self.range_.x - self.pos.x

        if start.y == 0:
            end.y += self.range_.y - self.pos.y

        if end.x > self.matrix.size.i.x:
            start.x -= (
                end.x - self.frame.size.i.x + 2
            )  # ? Adds a row of spaces on the top and bottom
            end.x = self.matrix.size.i.x

        if end.y > self.matrix.size.i.y:
            start.y -= end.y - self.matrix.size.i.y
            end.y = self.matrix.size.i.y

        rows = self.matrix[start:end].rows

        # add a column of spaces to each side
        for row in rows:
            row.insert(0, Cell(" "))
            row.append(Cell(" "))

        f = Frame(Matrix(rows))
        f.update()
        return f

    def link(self, map_: Self, exit: Coord, entrance: Coord):
        """Link a map to another map through a exit and entrance."""
        self.exits[exit] = (map_, entrance)
        map_.exits[entrance] = (self, exit)

    def _update_player(self, og):
        # m.exits[Coord(2, 19)] = (m, Coord(4, 26))
        
        self.frame[self.previous].value = " "  # (use base map in future)

        self.frame.update()
        
        

        # self.scene.draw()

        self.previous = copy(self.pos)
       
        
        self.frame[self.pos].value = self.player_char
        #self.frame[self.pos].value = " "  # (use base map in future)

        for key in Keyboard.pressed_keys.copy():
            if key == "w":
                self.up()
            elif key == "a":
                self.left()
            elif key == "s":
                self.down()
            elif key == "d":
                self.right()

        if not self.is_valid(self.pos):
            self.pos = self.previous
            if self.pos in self.exits:
                map_, pos = self.exits[self.pos]

                if not og:
                    return True

                if map_ is not None:
                    # logger.debug(f"running {map_} on {pos}")
                    map_(pos)
                    self.exits[self.pos] = map_, Coord(
                        2, 19
                    )  # got to reset the exits cause it changes with your pos for some reason

    last_coords = []

    def _update_weather(self, weather):  # TODO fix glitching
        for coord in Map.last_coords:
            self.frame[coord].value = " "  # (use base map in future)

        particles = choices(weather.particles, k=weather.heaviness)

        # self.open_cells.remove(self.pos)
        coords = choices(self.open_cells, k=weather.heaviness)
        # self.open_cells.append(self.pos)

        for coord, particle in list(zip(coords, particles)):
            self.frame[coord].value = particle

        Map.last_coords = coords

    def _play_weather(self):
        for weather in Weather.active:
            if weather.sound is not None:
                weather.sound.fade_in()

    def __call__(self, entrance: Coord = ..., og=False):
        if entrance is not ...:
            self.pos = entrance

        self._play_weather()

        EventGroup(
            [
                Event(self._update_player, 0.1, og),
                *[
                    Event(self._update_weather, weather.frequency, weather)
                    for weather in Weather.active
                    if weather.particles is not None
                ],
            ]
        ).play()

    def up(self, times: int = 1):
        self.pos.y -= times

    def down(self, times: int = 1):
        self.pos.y += times

    def left(self, times: int = 1):
        self.pos.x -= times

    def right(self, times: int = 1):
        self.pos.x += times

    def is_valid(self, pos: Coord) -> bool:
        try:
            if (
                self.matrix[pos].collision
                or pos.x >= self.matrix.size.x
                or pos.y >= self.matrix.size.y  # > or >= +1
            ):
                return False
        except IndexError:
            return False
        return True


m = Map(
    Frame.map(
        """
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
""",
        border_type=Borders.THIN,
    ),
    Coord(5, 5),
)


m2 = Map(
    Frame.map(
        """
HOME____________________________
|  _____  | []             |    |
|  |   |  | []             |____|
|  |   |__| []             |====|
|__|                       |====|
|      X                        |
|                               |
                      () ____   |
|                        [==]   |
|     __              [|      | |
| [= |__| =]          [|  ()  | |
|                     [|      | |
|_______________________________|"""
    ),
    Coord(5, 29),
)

# m2.link(m, Coord(4, 26), Coord(2, 19))

# m.exits[Coord(1, 19)] = (m2, Coord(5, 31))
# m2.exits[Coord(5, 28)] = (m, Coord(2, 19))


Screen.clear()
f = Frame.box(Size(20, 50))
f2 = Frame.box(Size(10, 25))
# f2.events = [Event(m._update_player, 0.1, False)]
m.frame.events = [Event(m._update_player, 0.1, False)]
f.add_frame(m.frame)

# all_events = []
# for frame in f.all_frames:
#     if frame.events:
#         all_events += frame.events
with key_listener:
    EventGroup(
        [frame.events[0] for frame in f.all_frames]
        + [
            Event(m._update_weather, weather.frequency, weather)
            for weather in Weather.active
            if weather.particles is not None
        ]
    ).play()


# EventGroup(
#     [
#         Event(self._update_player, 0.1, og),
#         *[
#             Event(self._update_weather, weather.frequency, weather)
#             for weather in Weather.active
#             if weather.particles is not None
#         ],
#     ]
# ).play()

# with key_listener:
#     m2(og=True)
