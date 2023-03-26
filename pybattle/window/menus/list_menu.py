from math import ceil

from pybattle.ansi.colors import Colors, ColorType
from pybattle.types_ import Align
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Cell, Matrix, level_out
from pybattle.window.grid.range import RectRange
from pybattle.window.grid.size import Size
from pybattle.window.menus.menu import Menu, Selection


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

        self._frame = frame

        selections = [
            "".join([cell.value for cell in row])
            for row in Matrix(selections, alignment=self.alignment).rows
        ]
        size = Size("\n".join(selections))

        new_selections = []
        for i, selection in enumerate(selections):
            rect_range = RectRange.center_range(self._frame.inner_size, size)
            coord = Coord(rect_range.start.y + i, rect_range.start.x)
            new_selections.append(Selection(selection, coord))
        self.selections: list[Selection] = new_selections

        self.selection = self.selections[0]

    @property
    def frame(self):
        for selection in self.selections:
            if selection == self.selection:
                self._frame.contents[
                    selection.location : selection.location + selection.size
                ] = Matrix(
                    selection.label,
                    (self.default_color, RectRange(selection.size)),
                    alignment=self.alignment,
                )
            else:
                self._frame.contents[
                    selection.location : selection.location + selection.size
                ] = Matrix(selection.label, alignment=self.alignment)

        return self._frame
