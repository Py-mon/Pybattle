from time import sleep
from typing import Callable, Optional, Self

from pybattle.log.errors import Error
from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.border.border_type import Borders, BorderType, Direction
from pybattle.screen.frames.frame import Frame, get_box
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.matrix import Grid
from pybattle.screen.grid.nested import max_len
from pybattle.screen.grid.point import Coord, Size
from screen.window.window import keys_pressing
from pybattle.types_ import Alignment


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


class VoidSelection:
    """The base selection."""

    def __init__(
        self,
        label: str,
        color: Color = Colors.DEFAULT,
    ) -> None:
        self.label = label
        self.color = color

        self.pos = Coord(0, 0)

    @property
    def size(self):
        s = Size.from_str(self.label).i
        return s.add_y(1)


class Selection(VoidSelection):
    """A selection with a designated pos."""

    def __init__(
        self,
        label: str,
        pos: Coord,
        color: Color = Colors.DEFAULT,
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


class SwitchSelection:  # TODO clean up selections
    def __init__(
        self,
        off: VoidSelection | Selection | FrameSelection,
        selected: VoidSelection | Selection | FrameSelection,
    ) -> None:
        self.off = off
        self.selected = selected

        self.directions: dict[Self, list[Direction]] = {}

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


# class Selection:
#     def __init__(
#         self,
#         label: str,
#         color: Color = Colors.DEFAULT,
#     ) -> None:
#         self.label = label
#         self.color = color

#         self.pos = Coord(0, 0)

#     @property
#     def size(self):
#         return Size.from_str(self.label + " ")


# class FrameSelection:
#     """A selection that has a frame around it"""

#     def __init__(
#         self,
#         frame: Frame,
#     ) -> None:
#         self.frame = frame

#     @property
#     def size(self):
#         return self.frame.size


# class SwitchSelection:  # TODO clean up selections
#     def __init__(
#         self,
#         coord: Coord,
#         off: VoidSelection | Selection | FrameSelection,
#         selected: VoidSelection | Selection | FrameSelection,
#     ) -> None:
#         if off.pos != selected.pos:
#             raise Error("Cannot move a SwitchSelection's pos")
#         elif off.label != selected.label and off.label != "" and selected.label != "":
#             raise Error("Cannot change a SwitchSelection's label")

#         self.off = off
#         self.selected = selected

#         self.directions: dict[Self, list[Direction]] = {}

#     @property
#     def label(self):
#         return self.off.label

#     @label.setter
#     def label(self, label: str):
#         self.off.label = label
#         self.selected.label = label

#     @property
#     def pos(self):
#         return self.off.pos

#     @pos.setter
#     def pos(self, pos: Coord):
#         self.off.pos = pos
#         self.selected.pos = pos


# class Selection:
#     def __init__(
#         self,
#         label: str,
#         pos: Coord,
#         selected_color: Color,
#         unselected_color: Color = Colors.DEFAULT,
#     ) -> None:
#         self.selected = selected
#         self.unselected_color = unselected_color

#         self.directions: dict[Self, list[Direction]] = {}

#     @property
#     def label(self):
#         return self.selected.label

#     @property
#     def pos(self):
#         return self.selected.pos


# class FrameSelection:
#     def __init__(
#         self,
#         selected: Frame,
#         pos: Coord,
#         unselected_border_color: Color = Colors.DEFAULT,
#         unselected_inside_color: Color = Colors.DEFAULT,
#     ) -> None:
#         self.selected = selected
#         self.pos = pos
#         self.unselected_border_color = unselected_border_color
#         self.unselected_inside_color = unselected_inside_color

#         self.directions: dict[Self, list[Direction]] = {}


class Menu(Frame):
    def __init__(
        self,
        cells: tuple[tuple[Cell, ...], ...],
        selections: list[SwitchSelection],
        border_type: BorderType = Borders.THIN,
    ) -> None:
        super().__init__(cells, border_type)

        self.selections = selections

        # Set the starting selection to the one closest to the origin
        self.selection = self.selections[0]  # ? but not ordered?

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

    def update(self):
        for switch_selection in self.selections:
            if switch_selection == self.selection:
                selection = switch_selection.selected
            else:
                selection = switch_selection.off

            if isinstance(selection, FrameSelection):
                if selection.frame.border_color is not None:
                    selection.frame.color_border(selection.frame.border_color)
                if selection.frame.base_color is not None:
                    selection.frame.color_inner(selection.frame.base_color)
                self.add_frame(selection.frame, selection.pos)

            elif isinstance(selection, VoidSelection):
                self[selection.pos : selection.pos + selection.size] = Grid(
                    Cell.from_str(selection.label)
                )

                self.color(
                    selection.color,
                    (selection.size + selection.pos).rect_range(selection.pos),
                )

    def move(self, direction: Direction, times: int = 1) -> None:
        for _ in range(times):
            for selection, directions in self.selection.directions.items():
                if direction in directions:
                    self.selection = selection
                    break

    def switch(self):
        for key in keys_pressing:
            print(key)
            if key == "a":
                self.move(Direction.LEFT)
            elif key == "s":
                self.move(Direction.DOWN)
            elif key == "d":
                self.move(Direction.RIGHT)
            elif key == "w":
                self.move(Direction.UP)
            elif key == "Return":
                keys_pressing.remove(key)
                return self.selection

        self.update()

    @classmethod
    def centered_list(
        cls,
        cells: tuple[tuple[Cell, ...], ...],
        selections: list[SwitchSelection],
        align: Alignment = Alignment.MIDDLE,
    ) -> Self:
        labels = [selection.off.label for selection in selections]
        size = Size.from_str("\n".join(labels))

        for i, selection in enumerate(selections):
            selection.label = align.align(selection.label, size.width)

            slice_ = get_box(Size.from_iter(cells), size)
            selection.pos = Coord(slice_.start.y + i, slice_.start.x)

        menu = cls(cells, selections)

        # Link the first and the last item together
        selections[-1].directions[selections[0]].append(Direction.UP)
        selections[0].directions[selections[-1]].append(Direction.DOWN)

        return menu


# ╭─ Wind Bash ─ Air ─╮ ╭─ Slash ── Normal ─╮
# │ 50 STR    90% ACC │ │ 35 STR      20 EC │
# │ Physical    25 EC │ ╰───────────────────╯
# ╰───────────────────╯
# ╭─ Dodge ───────────╮ ╭─ Tornado ─── Air ─╮
# │ Support     30 EC │ │ 70 STR      50 EC │
# ╰───────────────────╯ ╰───────────────────╯
