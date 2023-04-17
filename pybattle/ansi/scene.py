from typing import Any, Self

from pybattle.ansi.screen import Screen
from pybattle.window.frames.frame import Frame
from pybattle.window.map.event import Event
from time import sleep


class Scene:
    _scenes: dict[str | int, Self] = {}
    amount = -1

    def __init__(self, frame: Frame, scene_reference: str | int = ...) -> None:
        self.frame = frame

        type(self).amount += 1
        if scene_reference == ...:
            type(self)._scenes[type(self).amount] = self
        else:
            type(self)._scenes[scene_reference] = self

    def show(self) -> Event:
        """Show the Scene"""
        Screen.clear()

        def loop():
            while True:
                Screen.write(self.frame)

                sleep(0.1)

        return Event(loop)

    def __class_getitem__(cls, item) -> Any:
        return cls._scenes[item]

    def __getitem__(self, item) -> Any:
        return self._scenes[item]
