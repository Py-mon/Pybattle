from typing import Optional

from pybattle.log import Logger
from pybattle.types_ import SizeReference
from pybattle.window.frames.frame import Frame
from pybattle.window.matrix import Matrix
from pybattle.window.size import Size


class CenteredFrame(Frame):
    """A Frame with text in the center."""

    def __init__(
        self,
        size: SizeReference,
        text: str | Matrix,
        title: Optional[str] = None,
    ) -> None:
        self.title = title

        self.size = Size(size)

        self.contents = Matrix(text)

        matrix = Matrix(self.inner_size)

        text_center = self.contents.size.center

        inner_frame_center = self.inner_size.center

        starting = inner_frame_center - text_center

        ending = inner_frame_center + text_center
        if self.contents.width % 2 == 1:
            ending = inner_frame_center + text_center + 1
            
        Logger.info_debug(repr(matrix))
        Logger.info_debug(repr(matrix[starting: ending]))
        Logger.info_debug(repr(self.contents))

        matrix[starting: ending] = self.contents

        self.contents = matrix

        self._update_frame()
