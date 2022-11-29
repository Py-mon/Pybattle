from asyncio import create_task, sleep
from random import randint
from typing import Callable, Optional

from src.window.matrix import Matrix
from src.window.screen import Screen
from src.window.frame import Frame
from keyboard import is_pressed


class Map:
    def __init__(
        self,
        map_: str,
        exits: Optional[list[tuple[int, int]]] = None,
        keys: Optional[dict[str, Optional[Callable[[], None]]]] = {'!': None, '?': None},
    ) -> None:
        self.base_matrix = Matrix(map_)
        self.matrix = Matrix(map_)
        
        self.row = 1
        self.column = 1

        self.__previous_row = 1
        self.__previous_column = 1

        self.keys = keys

        self.exits = exits

        self.collidables = [' ']
        
    @property
    def frame(self) -> Frame:
        return Frame(self.matrix)

    @property
    def location(self) -> tuple[int, int]:
        """The location of the player."""
        return (self.row, self.column)

    @property
    def previous_location(self) -> tuple[int, int]:
        """The previous location of the player."""
        return (self.__previous_row, self.__previous_column)

    def __str__(self) -> str:
        """The map."""
        return str(self.frame.matrix)

    def update_player(self) -> None:
        """Update the player to the screen."""
        try:
            if not self.collisions[self.row][self.column]:  # Hit Object
                self.row = self.__previous_row
                self.column = self.__previous_column
            else:
                self.matrix[self.previous_location] = self.base_matrix[self.location]
                self.__previous_row = self.row
                self.__previous_column = self.column
        except IndexError:  # Hit Bottom
            self.row = self.__previous_row
            self.column = self.__previous_column

        self.matrix[self.location] = 'x'

    # async def update_weather(self) -> None:
    #     for weather in Weather.active_weather:
    #         if weather.particle is not None and weather.speed is not None:
    #             columns = randint(1, len(self.collisions[0]) - 3)
    #             rows = randint(1, len(self.collisions) - 1)

    #             while not self.collisions[rows][columns]:
    #                 columns = randint(1, len(self.collisions[0]) - 3)
    #                 rows = randint(1, len(self.collisions) - 1)

    #             self.matrix[(rows, columns)] = weather.particle

    #             await sleep(weather.speed)

    #             self.matrix[(rows, columns)] = self.base_matrix[(rows, columns)]

    async def __call__(
        self,
        location: tuple[int, int],
        exits: Optional[list[tuple[int, int]]] = ...,
        keys: Optional[dict[str, Optional[Callable[[], None]]]] = ...
    ):
        if exits is ...:
            exits = self.exits
        if exits is None:
            exits = []

        if keys is ...:
            keys = self.keys
        if keys is None:
            keys = {}

        self.row = location[0]
        self.column = location[1]

        self.update_player()

        while self.location not in exits:
            # for _ in range(randint(8, 12)):
            #     create_task(self.update_weather())

            if is_pressed('w'):
                self.move_up()
                self.update_player()
            if is_pressed('d'):
                self.move_right()
                self.update_player()
            if is_pressed('s'):
                self.move_down()
                self.update_player()
            if is_pressed('a'):
                self.move_left()
                self.update_player()

            await sleep(.1)
            
            Screen.write(str(self), move_cursor=False)

    def move_up(self) -> None:
        """Move the player up once."""
        self.row -= 1

    def move_down(self) -> None:
        """Move the player down once."""
        self.row += 1

    def move_left(self) -> None:
        """Move the player left once."""
        self.column -= 1

    def move_right(self) -> None:
        """Move the player right once."""
        self.column += 1

    @property
    def collisions(self) -> list[list[bool]]:
        """A copy of the matrix that has True if it is collidable otherwise False."""
        return [[char in self.collidables for char in row] for row in self.matrix][:-1]
