from copy import copy
from time import sleep

from keyboard import is_pressed

from pybattle.ansi.scene import Scene
from pybattle.ansi.screen import Cursor, Screen
from pybattle.debug.log import Logger
from pybattle.window.frames.frame import Frame
from pybattle.window.frames.map_frame import MapFrame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Cell, Matrix
from pybattle.window.grid.size import Size
from pybattle.window.map.event import Event
from pybattle.window.menus.list_menu import ListMenu


class Map:
    def __init__(self, map_frame: MapFrame):
        self.map_frame = map_frame
        self.matrix = self.map_frame.contents

        self.pos = Coord(0, 0)

    def up(self, times: int = 1):
        self.pos.y -= times

    def down(self, times: int = 1):
        self.pos.y += times

    def left(self, times: int = 1):
        self.pos.x -= times

    def right(self, times: int = 1):
        self.pos.x += times

    def __call__(self, starting_location: Coord, sleep_time=5) -> Event:
        self.pos = starting_location

        def loop():
            while True:
                self.matrix[self.pos] = Cell(" ")

                previous = copy(self.pos)

                if is_pressed("w"):
                    self.up()
                if is_pressed("a"):
                    self.left()
                if is_pressed("s"):
                    self.down()
                if is_pressed("d"):
                    self.right()

                if not self.is_valid(self.pos):
                    self.pos = previous

                self.matrix[self.pos] = Cell("x")

                self.map_frame.update()

                sleep(0.1)

        return Event(loop)

    def is_valid(self, pos: Coord) -> bool:
        try:
            if (
                self.matrix[pos].collision
                or pos.x >= self.matrix.size.x
                or pos.y >= self.matrix.size.y + 1
            ):
                return False
        except IndexError:
            return False
        return True


class Map2(MapFrame):
    def __init__(self, map_frame: MapFrame):
        self.map_frame = map_frame
        self.matrix = self.map_frame.contents

        self.pos = Coord(0, 0)

    def up(self, times: int = 1):
        self.pos.y -= times

    def down(self, times: int = 1):
        self.pos.y += times

    def left(self, times: int = 1):
        self.pos.x -= times

    def right(self, times: int = 1):
        self.pos.x += times

    def __call__(self, starting_location: Coord, sleep_time=5) -> Event:
        self.pos = starting_location

        def loop():
            while True:
                self.matrix[self.pos] = Cell(" ")

                previous = copy(self.pos)

                if is_pressed("w"):
                    self.up()
                if is_pressed("a"):
                    self.left()
                if is_pressed("s"):
                    self.down()
                if is_pressed("d"):
                    self.right()

                if not self.is_valid(self.pos):
                    self.pos = previous

                self.matrix[self.pos] = Cell("x")

                self.map_frame.update()

                sleep(0.1)

        return Event(loop)

    def is_valid(self, pos: Coord) -> bool:
        try:
            if (
                self.matrix[pos].collision
                or pos.x >= self.matrix.size.x
                or pos.y >= self.matrix.size.y + 1
            ):
                return False
        except IndexError:
            return False
        return True


x = Map(
    MapFrame(
        """
                   ||||
                   ||||
                     ─┬─┬─┬─┬─


╭│╮   ╶─╮
│││    ░│
╰│╯   ╶─╯           ╭─────┬─╮
                    │░░░░░│▓│
                    ╰─────┴─╯ """
    )
)

z = x(Coord(3, 3))

y = ListMenu(Frame(Size(12, 30)), ["Inventory", "Menu", "Home"])

Event.from_frame(y.frame)


Scene(y.frame).show()


print(Event._events)

Event.play_all()


# class Map:
#     """Makes the given `matrix` into a map that the user can move around and interact with.

#     Use `__call__` to start the loop.
#     """
#     @staticmethod
#     def __is_empty(char: str) -> bool:
#         """Checks if `char` is a whitespace"""
#         return char == '─' or char == ' '

#     @staticmethod
#     def get_range(start, end) -> list[list[int]]:
#         lines = range(start[0], end[0] + 1) or [start[0]]
#         columns = range(start[1], end[1] + 1) or [start[1]]
#         return [[line, column] for line in lines for column in columns]

#     def __init__(self, map_: str, key: str = '!', item: Any = None) -> None:
#         self.map_ = Matrix(map_)

#         self.row = 1
#         self.column = 1

#         self.__previous_row = 1
#         self.__previous_column = 1

#         self.exits = []

#         self.key = key
#         self.item = item

#         self.__weather_channels = []

#     def __call__(self, starting_location: list[int], exits: list[list[int]], music: list[str] | None = None, wait_time: float = 0.125, volume: int = 100) -> None:
#         """Starts the loop that the player can move around the `map_`. Stops if the user's current `location` is in `exits`"""
#         self.volume = volume

#         self.play_weather(volume)
#         self.play_music(music, volume)

#         self.row = starting_location[0]
#         self.column = starting_location[1]

#         self.__previous_row = starting_location[0]
#         self.__previous_column = starting_location[1]

#         self.map_.matrix[self.row][self.column] = 'x'
#         print(self.map_)

#         print('\n\n\n')
#         print('\033[3A')

#         starting_time = time()

#         while not any([self.row == exit_[0] and self.column == exit_[1] for exit_ in exits]):
#             self.update()

#             self.__press('w', self.move_up)
#             self.__press('a', self.move_left)
#             self.__press('s', self.move_down)
#             self.__press('d', self.move_right)

#             difference = round(time() - starting_time)
#             timer = 59 - difference
#             print('TIME LEFT:', timer, '')
#             if timer <= 0:
#                 exit()

#             sleep(wait_time)

#     def __press(self, key: str, func) -> None:
#         """If `key` is held down it updates the screen and runs `func`"""
#         if is_pressed(key):
#             self.update()

#             func()
#             self.validate_location()

#     def play_music(self, music, volume) -> None:
#         if music is not None:
#             mixer.music.load(music)
#             mixer.music.set_volume(volume / 100)
#             mixer.music.play(-1)

#     def pause_music(self) -> None:
#         mixer.music.pause()

#     def unpause_music(self) -> None:
#         mixer.music.unpause()

#     def play_weather(self, volume) -> None:
#         for index, weather in enumerate(Weather.active_weather):
#             if weather.sound is not None:
#                 sound = mixer.Sound(weather.sound)
#                 sound.set_volume(volume / 100)
#                 channel = mixer.Channel(index)
#                 self.__weather_channels.append(channel)
#                 channel.play(sound, -1)

#     def pause_weather(self) -> None:
#         for channel in self.__weather_channels:
#             channel.pause()

#     def unpause_weather(self) -> None:
#         for channel in self.__weather_channels:
#             channel.unpause()

#     def update(self) -> None:
#         """Updates the screen by drawing the weather particles and the players position. Removes particles after printing the screen"""
#         particles = []
#         for weather in Weather.active_weather:
#             if weather.particle is not None or weather.amount is not None:
#                 for _ in range(weather.amount):
#                     x = [randint(1, len(self.map_.matrix) - 2),
#                          randint(1, len(self.map_.matrix[0]) + 20)]
#                     while not self.collisions[x[0]][x[1]]:
#                         x = [randint(1, len(self.map_.matrix) - 2),
#                              randint(1, len(self.map_.matrix[0]) + 20)]
#                     particles.append(x)
#                 for particle in particles:
#                     self.map_.matrix[particle[0]
#                                      ][particle[1]] = weather.particle

#         while len(self.map_.matrix) > get_terminal_size().lines - 1:
#             self.pause_weather()
#             self.pause_music()
#         self.unpause_weather()
#         self.unpause_music()

#         self.map_.matrix[self.row][self.column] = 'x'
#         print(f'\033[{len(self.map_.matrix) + 2}A')  # Moves the cursor up
#         print(self.map_)

#         for particle in particles:
#             self.map_.matrix[particle[0]][particle[1]
#                                           ] = self.map_.base_matrix[particle[0]][particle[1]]

#     def validate_location(self) -> None:
#         """Check whether the `self.row` and `self.column` are a valid location (False in `collisions`). If not a valid location moves the user back"""
#         try:
#             if not self.collisions[self.row][self.column]:  # Hit Object
#                 if self.map_.matrix[self.row][self.column] == self.key:
#                     if self.item is not None:
#                         self.pause_weather()
#                         mixer.Sound(r'sounds\pick_up.wav').play()

#                         speech_box(f'You found a {self.item.name}!', height=1, width=len(
#                             self.map_.matrix[0]) - 6, message='PRESS SPACE TO CONTINUE')
#                         self.map_.base_matrix[self.row][self.column] = ' '
#                         self.map_.matrix[self.row][self.column] = ' '
#                         self.item = None
#                         self.unpause_weather()

#                 self.row = self.__previous_row
#                 self.column = self.__previous_column
#             else:
#                 self.map_.matrix[self.__previous_row][self.__previous_column] = self.map_.base_matrix[self.__previous_row][self.__previous_column]
#                 self.__previous_row = self.row
#                 self.__previous_column = self.column
#         except IndexError:  # Hit Bottom
#             self.row = self.__previous_row
#             self.column = self.__previous_column

#     def move_up(self) -> None:
#         """Subtracts 1 from `self.row` moving the player up"""
#         self.row -= 1

#     def move_down(self) -> None:
#         """Adds 1 to `self.row` moving the player down"""
#         self.row += 1

#     def move_left(self) -> None:
#         """Subtracts 1 from `self.columns` moving the player left"""
#         self.column -= 1

#     def move_right(self) -> None:
#         """Adds 1 to `self.column` moving the player right"""
#         self.column += 1

#     @property
#     def collisions(self) -> list[list[bool]]:
#         """A Matrix (2D array), of `map_` on each element, if it is a whitespace"""
#         return [[self.__is_empty(char) for char in row] for row in self.map_.matrix][:-1]
