from copy import copy
from random import choice, choices, randint
from time import sleep, time
from typing import Annotated, Any, Callable, Optional, Self

from keyboard import is_pressed
from window.screen.scene import Scene

from pybattle.ansi.cursor import Cursor
from pybattle.log.log import Logger, logger
from pybattle.types_ import CardinalDirection
from pybattle.window.event import Event, EventExit, EventGroup
from pybattle.window.frames.border.border_type import Borders
from pybattle.window.frames.frame import Frame
from pybattle.window.frames.menu import Menu
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Cell, Matrix
from pybattle.window.grid.size import Size
from pybattle.window.map.weather import Rain, Weather

# u = Rain(CardinalDirection.WEST)
# print(u.particles)
Weather(particles=["*", "."], heaviness=2, frequency=0.08)


class Map:
    def __init__(
        self,
        map_: Frame,
        starting_pos: Coord,
        exits: list[Coord] = [],
        player_char: str = "𓀞",  # 'º ⏺ ○ ● ◯ ☃ ☹ ☻ ☺ ♀ ♂ ⚬ ⚲ ⚴ ⛑ ⛹ ⫯ x X' 𓀞
    ):
        self.frame = map_
        self.matrix = self.frame.contents

        self.exits: dict[Coord, tuple[Optional[Self], ellipsis | Coord]] = {}
        for exit in exits:
            self.exits[exit] = (None, ...)

        self.pos = starting_pos
        self.range_ = Size(3, 10)
        self.player_char = player_char

        self.closed: bool = True

        self.open_cells = []
        for coord in self.frame.matrix.coords:
            if not self.frame[coord].collision:
                self.open_cells.append(coord)

        self.scene = Scene(self.camera)

    def camera(self):
        end = self.pos + self.range_
        start = self.pos - self.range_

        if start.x == 0:
            end.x += self.range_.x - self.pos.x

        if start.y == 0:
            end.y += self.range_.y - self.pos.y

        if end.x > self.matrix.size.i.x:
            start.x -= end.x - self.frame.size.i.x + 2  # works???
            end.x = self.matrix.size.i.x

        if end.y > self.matrix.size.i.y:
            start.y -= end.y - self.matrix.size.i.y
            end.y = self.matrix.size.i.y

        rows = self.matrix[start:end].rows

        # add a column of spaces to each side
        for row in rows:
            row.insert(0, Cell(" "))
            row.append(Cell(" "))

        return Frame(Matrix.from_iter(rows))

    def link(self, map_: Self, exit: Coord, entrance: Coord):
        """Link a map to another map through a exit and entrance."""
        self.exits[exit] = (map_, entrance)
        map_.exits[entrance] = (self, exit)

    def _update_player(self):
        # m.exits[Coord(2, 19)] = (m, Coord(4, 26))

        self.matrix[self.pos].value = self.player_char

        self.frame.update()

        sleep(0.1)

        self.previous = copy(self.pos)

        self.matrix[self.pos].value = " "  # (use base map in future)

        if is_pressed("w"):
            self.up()
        if is_pressed("a"):
            self.left()
        if is_pressed("s"):
            self.down()
        if is_pressed("d"):
            self.right()

        if not self.is_valid(self.pos):
            self.pos = self.previous
            # print(self.pos, self.exits)
            logger.debug((self.pos, self.exits))
            if self.pos in self.exits:
                map_, pos = self.exits[self.pos]
                if map_ is not None:
                    self.events.events[1].stop()
                    # Event.stop_all()  # stops the _update_thread so, doesnt finish :( (maybe pause the thread)

                    map_event = map_(pos)

                    map_event.play() # add on this one's update a break on exit
                    print("EXIT")

                    # self.events.events[1].stopped = False
                    # self.events.events[1].start()
                    def update():
                        sleep(0.01)
                        Scene.refresh(1)

                    Event(update).start()
                    self().play()

                    # Event(self.scene.add).start()

    def _update_weather(self):
        if Weather.active:
            for weather in Weather.active:
                if weather.particles is not None:
                    particles = choices(weather.particles, k=weather.heaviness)

                    # self.open_cells.remove(self.pos)
                    coords = choices(self.open_cells, k=weather.heaviness)
                    # self.open_cells.append(self.pos)

                    # matrix = copy(self.frame.matrix)

                    for coord, particle in list(zip(coords, particles)):
                        self.frame[coord].value = particle

                    sleep(weather.frequency)

                    for coord in coords:
                        self.frame[coord].value = " "  # (use base map in future)
        else:
            return EventExit.Silent

    def _init(self):
        for weather in Weather.active:
            if weather.sound is not None:
                weather.sound.fade_in(3)

    def __call__(self, entrance: Coord = ...) -> EventGroup:
        if entrance is not ...:
            self.pos = entrance

        self.events = EventGroup(
            self._update_player,
            # self._update_weather,
            self.scene.add,
            # init=self._init,
        )

        return self.events

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
        border_type=Borders.THICK,
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

m.exits[Coord(2, 19)] = (m2, Coord(4, 26))
m2.exits[Coord(4, 26)] = (m, Coord(2, 19))


def update():
    sleep(0.01)
    Scene.refresh(1)


Event(update).start()

Scene.clear()


print(m.exits, m2.exits)

m2().play()
