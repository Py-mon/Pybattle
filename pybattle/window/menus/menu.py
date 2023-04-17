from keyboard import is_pressed
from pygame import time

from pybattle.ansi.colors import Colors, ColorType
from pybattle.ansi.screen import Screen
from pybattle.window.frames.border.border_type import Direction
from pybattle.window.frames.center_frame import CenteredFrame
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.size import Size
from pybattle.window.grid.range import RectRange
from pybattle.window.map.event import Event
from time import sleep


def get_directions(from_: Coord, to: Coord) -> list[Direction]:
    directions = []

    y1, x1 = from_
    y2, x2 = to

    if y1 < y2:
        directions.append(Direction.DOWN)
    if y1 > y2:
        directions.append(Direction.UP)

    if x1 < x2:
        directions.append(Direction.RIGHT)
    if x1 > x2:
        directions.append(Direction.LEFT)

    return directions


class Selection:
    def __init__(self, label: str, location: Coord, size: Size = ...) -> None:
        self.location = location
        self.label = label

        if size is ...:
            self.size = Size.from_str(label) - 1
        else:
            self.size = size
            
    def __repr__(self):
        return self.label



class Menu:
    def __init__(
        self,
        frame: Frame,
        selections: list[Selection],
        default_color: ColorType = Colors.BLUE,
    ) -> None:
        self.default_color = default_color
        self.selections = selections

        self.selection = selections[0]

        self.frame = frame

        self._event()

    def update(self):
        for selection in self.selections:
            if selection == self.selection:
                self.frame.add_frame(
                    CenteredFrame(
                        selection.size,
                        selection.label,
                        colors=[
                            (self.default_color, RectRange(Coord(self.selection.size)))
                        ],
                    ),
                    selection.location,
                )
            else:
                self.frame.add_frame(
                    CenteredFrame(selection.size, selection.label), selection.location
                )

        self.frame.update()

    def sort(self, dirs):
        # Sort the dirs & self.selections by dirs
        x = list(zip(dirs, self.selections))
        x.sort(key=lambda x: x[0])

        self.selections = [c[1] for c in x]
        return [c[0] for c in x]

    @property
    def directions(self) -> list[list[Direction]]:
        return self.sort(
            [
                get_directions(self.selection.location, selection.location)
                for selection in self.selections
            ]
        )

    def move(self, direction: Direction) -> None:
        for i, directions in enumerate(self.directions):
            if direction in directions:
                self.selection = self.selections[i]
                break

    def right(self) -> None:
        self.move(Direction.RIGHT)

    def left(self) -> None:
        self.move(Direction.LEFT)

    def up(self) -> None:
        self.move(Direction.UP)

    def down(self) -> None:
        self.move(Direction.DOWN)

    def _event(self) -> None:
        def loop(_):
            while True:
                self.update()

                if is_pressed("right"):
                    self.right()
                elif is_pressed("left"):
                    self.left()
                elif is_pressed("up"):
                    self.up()
                elif is_pressed("down"):
                    self.down()
                elif is_pressed("enter"):
                    return self.selection

                sleep(0.1)

        self.frame.event = loop
