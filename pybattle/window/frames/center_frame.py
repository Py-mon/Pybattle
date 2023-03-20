from math import ceil, floor
from typing import Optional

from pybattle.ansi.colors import Colors, ColorType
from pybattle.debug.log import Logger
from pybattle.types_ import Align, ColorRange
from pybattle.window.frames.border.border_type import Borders, BorderType
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Matrix
from pybattle.window.grid.size import Size
from pybattle.window.grid.range import RectRange


class CenteredFrame(Frame):
    """A Frame with text in the center."""

    def __init__(
        self,
        size: Size,
        text: str,
        title: Optional[str] = None,
        alignment: Align = Align.CENTER,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        colors: list[ColorRange] = [],
        text_colors: list[ColorRange] = [],
    ) -> None:
        super().__init__(size, title, border_color, title_color, border_type)
        
        self.contents = Matrix(text, *text_colors, alignment=alignment)

        matrix = Matrix(self.inner_size)

        center_range = RectRange.center_range(self.inner_size, self.contents.size)
        
        Logger.debug(repr(matrix[center_range]))
        Logger.debug(repr(self.contents))

        matrix[center_range] = self.contents
        
        matrix.add_colors(*self.contents.colors)

        self.contents = matrix
        
        self._construct_frame()
        
        Logger.debug(repr(self.matrix))
        
        self.contents.add_colors(*colors)


CenteredFrame(Size(10, 20), 'hi\nhello')