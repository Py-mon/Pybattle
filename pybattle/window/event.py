from math import ceil
from time import sleep
from typing import Any, Optional

from pybattle.ansi.cursor import Cursor
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Matrix
from pybattle.window.grid.size import Size
from pybattle.window.screen.screen import Screen


class Scene:
    def __init__(self, scene: Any, pos: Coord = ..., max_size: Optional[Size] = None):
        self.max_size = max_size

        self.scene = str(scene)
        self.pos = pos

        if self.pos is ...:
            self.pos = Cursor.pos

    def draw(self):
        if self.max_size is not None:
            Screen.rect_print(Matrix.from_size(self.max_size), self.pos)

        Screen.rect_print(self.scene, self.pos)


class Event:
    fps = 30
    events = []

    def __init__(self, func, sleep):
        """Minimum sleep 0.03"""
        self.every_frames = ceil(type(self).fps * sleep)
        self.func = func

        type(self).events.append(self)

    @classmethod
    def play(cls):
        frame_count = 0

        while True:
            sleep(1 / cls.fps)
            frame_count += 1

            for event in cls.events:
                if frame_count % event.every_frames == 0:
                    event.func()


# S.clear()
# Cursor.move(Coord(1, 1))
# rect_print("hello\nworld")


Screen.clear()

z = 105


def x():
    global z
    z -= 1
    Scene(str(z), Coord(0, 0), Size(1, 3)).draw()


def y():
    Scene("y", Coord(2, 2)).draw()


Event(x, 1)
Event(y, 3)
Event.play()

