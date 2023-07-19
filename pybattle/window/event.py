from collections.abc import Callable
from inspect import isfunction, ismethod
from math import ceil
from time import sleep
from typing import Any, Optional

from pybattle.ansi.cursor import Cursor
from window.text.grid.point import Coord
from pybattle.window.text.grid.matrix import Matrix
from pybattle.window.text.grid.size import Size
from pybattle.window.screen.screen import Screen


class Scene:
    def __init__(
        self,
        scene: Callable[[], Any],
        pos: Coord = ...,
        max_size: Optional[Size] = None,
    ):
        self.max_size = max_size

        self.scene = scene

        self.pos = pos

        if self.pos is ...:
            self.pos = Cursor.pos

    def draw(self):
        if self.max_size is not None:
            Screen.rect_print(Matrix.from_size(self.max_size), self.pos)

        Screen.rect_print(str(self.scene()), self.pos)


class Speed:
    TIME = 1


class Event:
    fps = 30

    def __init__(self, func, every, *args, time_affected: bool = True):
        """Minimum sleep 0.03 with 30 fps"""
        if time_affected:
            every /= Speed.TIME

        self.every_frames = ceil(type(self).fps * every)
        self.func = func
        self.args = args


class EventGroup:
    def __init__(self, events: list[Event]):
        self.events = events

    def play(self):
        frame_count = 0

        event2 = False
        while not event2:
            sleep(1 / Event.fps)
            frame_count += 1

            if not self.events:
                break

            for event in self.events:
                if frame_count % event.every_frames != 0:
                    continue

                event2 = event.func(*event.args)
