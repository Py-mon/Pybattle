from time import sleep
from typing import Optional, Self

from keyboard import is_pressed

from pybattle.ansi.colors import Colors, ColorType
from pybattle.ansi.screen import Screen
from pybattle.types_ import ColorRange
from pybattle.window.frames.base_frame import Frame
from pybattle.window.frames.border.border_type import Borders, BorderType, Direction
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.range import RectRange
from pybattle.window.grid.size import Size
from pybattle.window.map.event import Event


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


class Menu:
    def __init__(
        self,
        size: Size,
        selections: list[tuple[Frame, Coord]],
        title: Optional[str] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        selected_border_color: ColorType = Colors.RED,
        selected_label_color: ColorType = Colors.BLUE,
        colors: list[ColorRange] = [],
    ) -> None:
        def loop(self: Self):
            while True:
                self._update1()

                if is_pressed("right"):
                    print("right")
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

        self.frame = Frame.box(
            size.inner,
            title,
            loop,
            border_color,
            title_color,
            border_type,
            colors,
        )

        self.selected_border_color = selected_border_color
        self.selected_label_color = selected_label_color

        self.selections = selections
        self.selection = selections[0]

        self._update1()

    def _update1(self):
        for selection in self.selections:
            frame, location = selection
            if selection == self.selection:
                frame.border_color = self.selected_border_color
                frame.contents.add_color(
                    self.selected_label_color, RectRange(frame.size.inner - 1)
                )
            else:
                frame.border_color = Colors.DEFAULT
                frame.contents.add_color(
                    Colors.DEFAULT, RectRange(frame.size.inner - 1)
                )

            frame.update()

            self.frame.add_frame(frame, location)

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
                get_directions(self.selection[1], selection[1])
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


# x.add_frame(Frame.centered("play", Size(4, 6)), Coord(1, 1))
# print(x)
m = Menu(
    Size(7, 20),
    [
        (Frame.centered("play", Size(4, 6)), Coord(1, 1)),
        (Frame.centered("quit", Size(4, 6)), Coord(1, 7)),
    ],
)

Event.from_frame(m.frame)


def loop():
    while True:
        Screen.write(m.frame)


Event(loop)

print(Event._events)
Event.play_all()
