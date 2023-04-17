from math import ceil

from pybattle.ansi.colors import Colors, ColorType
from pybattle.types_ import Align
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Cell, Matrix
from pybattle.window.grid.range import RectRange
from pybattle.window.grid.size import Size
from pybattle.window.menus.menu import Menu, Selection
from pybattle.window.map.event import Event


class ListMenu(Menu):
    def __init__(
        self,
        frame: Frame,
        selections: list[str],
        alignment: Align = Align.CENTER,
        default_color: ColorType = Colors.BLUE,
    ) -> None:
        self.default_color = default_color

        self.alignment = alignment

        self.frame = frame

        # Align Selections
        selections = [
            "".join([cell.value for cell in row])
            for row in Matrix(selections, alignment=self.alignment).rows
        ]
        size = Size("\n".join(selections))

        # Position the Selections in the Center
        new_selections = []
        for i, selection in enumerate(selections):
            rect_range = RectRange.center_range(self.frame.inner_size, size)
            coord = Coord(rect_range.start.y + i, rect_range.start.x)
            new_selections.append(Selection(selection, coord))
        self.selections: list[Selection] = new_selections

        self.selection = self.selections[0]

        self._event()

    def update(self):
        for selection in self.selections:
            if selection == self.selection:
                self.frame.contents[
                    selection.location : selection.location + selection.size
                ] = Matrix(
                    selection.label,
                    (self.default_color, RectRange(selection.size)),
                    alignment=self.alignment,
                )
            else:
                self.frame.contents[
                    selection.location : selection.location + selection.size
                ] = Matrix(selection.label, alignment=self.alignment)

        self.frame.update()
