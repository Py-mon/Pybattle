from typing import Optional

from pybattle.debug.log import Logger
from pybattle.window.frames.frame import Frame
from pybattle.window.grid.matrix import Matrix
from pybattle.window.grid.size import Size
from pybattle.ansi.colors import ColorType, Colors
from pybattle.window.frames.border_type import Borders, BorderType
from pybattle.window.grid.coord import Coord


class CenteredFrame(Frame):
    """A Frame with text in the center."""

    def __init__(
        self,
        size: Size,
        text: str,
        title: Optional[str] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        colors: list[tuple[Coord, ColorType]] = []
    ) -> None:
        super().__init__(size, title, border_color, title_color, border_type)

        self.contents = Matrix(text)
        self.contents.add_colors(*colors)

        matrix = Matrix(self.inner_size)

        text_center = self.contents.size.center

        inner_frame_center = self.inner_size.center

        starting = inner_frame_center - text_center
        ending = inner_frame_center + text_center

        # if self.contents.width % 2 == 1:
        #     ending = inner_frame_center + text_center + 1
        # if self.contents.width % 2 == 0:
        #     ending.x += 1
            
        Logger.info_debug(repr(matrix))
        Logger.info_debug(repr(matrix[starting: ending]))
        Logger.info_debug(repr(self.contents))
        
        matrix[starting: ending] = self.contents
        
        matrix.colors += self.contents.colors

        self.contents = matrix
        
        self._construct_frame()
