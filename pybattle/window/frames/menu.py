from time import sleep
from typing import Callable, Self

from keyboard import is_pressed
from window.event import Event
from window.frames.frame import Frame

from pybattle.ansi.colors import Colors, ColorType
from pybattle.log.errors import Error
from pybattle.types_ import Align
from pybattle.window.frames.border.border_type import Direction
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Matrix
from pybattle.window.grid.range import RectRange
from pybattle.window.grid.size import Size


def get_directions(from_: Coord, to: Coord) -> set[Direction]:
    directions = set()

    y1, x1 = from_
    y2, x2 = to

    if y1 < y2:
        directions.add(Direction.DOWN)
    if y1 > y2:
        directions.add(Direction.UP)

    if x1 < x2:
        directions.add(Direction.RIGHT)
    if x1 > x2:
        directions.add(Direction.LEFT)

    return directions


class VoidSelection:
    """The base selection"""

    def __init__(
        self,
        label: str,
        color: ColorType = Colors.DEFAULT,
    ) -> None:
        self.label = label
        self.color = color

        self.pos = Coord()

    @property
    def size(self):
        return Size.from_str(self.label).i


class Selection(VoidSelection):
    """A selection with a designated pos"""

    def __init__(
        self,
        label: str,
        pos: Coord,
        color: ColorType = Colors.DEFAULT,
    ) -> None:
        super().__init__(label, color)

        self.pos = pos


class FrameSelection(Selection):
    """A selection that has a frame around it"""

    def __init__(
        self,
        frame: Frame,
        pos: Coord,
    ) -> None:
        super().__init__("", pos)

        self.frame = frame

    @property
    def size(self):
        return self.frame.size


class SwitchSelection:
    def __init__(
        self,
        off: VoidSelection | Selection | FrameSelection,
        selected: VoidSelection | Selection | FrameSelection,
    ) -> None:
        if off.pos != selected.pos:
            raise Error("Cannot move a SwitchSelection's pos")
        elif off.label != selected.label and off.label != "" and selected.label != "":
            raise Error("Cannot change a SwitchSelection's label")

        self.off = off
        self.selected = selected

        self.directions: dict[Self, set[Direction]] = {}

    def __class_getitem__(cls, x):
        pass

    @property
    def label(self):
        return self.off.label

    @label.setter
    def label(self, label: str):
        self.off.label = label
        self.selected.label = label

    @property
    def pos(self):
        return self.off.pos

    @pos.setter
    def pos(self, pos: Coord):
        self.off.pos = pos
        self.selected.pos = pos


class Menu:
    def __init__(
        self,
        frame: Frame,
        selections: list[SwitchSelection],
    ) -> None:
        self.frame = frame

        self.selections = selections

        # Set the starting selection to the one closest to the origin
        self.selection = selections[0]

        for current_selection in self.selections.copy():
            # Sort the selections by the closest ones first (when you press '►' it will go to the closest one to the right)
            self.selections.sort(key=lambda x: current_selection.pos.distance(x.pos))
            for selection in self.selections:
                # Exclude its own selection
                if selection != current_selection:
                    # Add the directions at the selected point to the other selection
                    current_selection.directions[selection] = get_directions(
                        current_selection.pos, selection.pos
                    )

        self.update()

        def event():
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
                return self.selection.label

            sleep(0.1)

        self.event = event

    def update(self):
        frames = []
        for switch_selection in self.selections:
            if switch_selection == self.selection:
                selection = switch_selection.selected
            else:
                selection = switch_selection.off

            if isinstance(selection, FrameSelection):
                frames.append((selection.frame, selection.pos))

                selection.frame.update(
                    selection.frame.border_color,
                    base_color=selection.frame.base_color,
                )

            elif isinstance(selection, VoidSelection):
                self.frame.contents[
                    selection.pos : selection.pos + selection.size
                ] = Matrix.from_str(selection.label)

                self.frame.contents.color(
                    selection.color,
                    RectRange(selection.pos + selection.size),
                )
        
        self.frame.update(frames=frames + self.frame.frames)

    def move(self, direction: Direction) -> None:
        for selection, directions in self.selection.directions.items():
            if direction in directions:
                self.selection = selection
                break

    def right(self) -> None:
        self.move(Direction.RIGHT)

    def left(self) -> None:
        self.move(Direction.LEFT)

    def up(self) -> None:
        self.move(Direction.UP)

    def down(self) -> None:
        self.move(Direction.DOWN)

    @classmethod
    def centered_list(
        cls,
        frame: Frame,
        selections: list[SwitchSelection[VoidSelection]],
        align: Align = Align.MIDDLE,
    ) -> Self:
        labels = [selection.off.label for selection in selections]
        max_ = max(len(label) for label in labels)
        size = Size.from_str("\n".join(labels))
        size.x = max_

        for i, selection in enumerate(selections):
            print(repr(selection.label))
            selection.label = align.align(selection.label, max_)
            print(repr(selection.label))
            rect_range = RectRange.center_range(frame.size.inner, size)
            selection.pos = Coord(rect_range.start.y + i, rect_range.start.x)

        menu = cls(frame, selections)

        # Link the first and the last item together
        selections[-1].directions[selections[0]].add(Direction.UP)
        selections[0].directions[selections[-1]].add(Direction.DOWN)

        return menu
