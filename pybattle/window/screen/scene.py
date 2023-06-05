from os import name as os_name
from os import system
from shutil import get_terminal_size
from time import sleep
from typing import Any, Callable, Optional

from pybattle.ansi.colors import ColorType
from pybattle.ansi.cursor import Cursor
from pybattle.window.event import Event, EventGroup
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size


# TODO fix switching sides
class Scene:
    scenes: dict[str, Coord] = {}

    def __init__(self, get_scene: Callable[[], Any], pos: Coord = ...) -> None: # TODO fix POS
        self.get_scene = get_scene
        self.pos = pos

    def add(self) -> None:
        """Add the scene to be printed."""
        self.scenes[self.get_scene()] = self.pos
        sleep(0.01)

    @classmethod
    def refresh(
        cls,
        len_: int = 0,
    ) -> None:
        """Print all the scenes."""
        if len(cls.scenes) == len_:
            for scene, pos in cls.scenes.copy().items():
                for line in str(scene).splitlines():
                    if pos is ...:
                        pos = Cursor.pos

                    pos.y += 1
                    Cursor.move(pos)

                    print(line)

        Cursor.move(Coord(0, 0))
        cls.scenes = {}

    @staticmethod
    def clear() -> None:
        """Clear the screen. Works on all operating systems"""
        system("cls" if os_name == "nt" else "clear")

    @staticmethod
    def terminal_size() -> Size:
        return Size(*get_terminal_size())


# q = 0


# def get_x():
#     global q
#     q += 1
#     return q


# def get_y():
#     sleep(0.009)
#     return "Nothing"


# def refresh():
#     sleep(0.01)
#     Scene.refresh(1)


# import keyboard


# def update():
#     if keyboard.is_pressed("p"):
#         Event.stop_all()
#         EventGroup(Scene(get_x).add, refresh).play()


# Scene.clear()
# Cursor.move(Coord(0, 0))

# EventGroup(Scene(get_y).add, refresh, update).play()
