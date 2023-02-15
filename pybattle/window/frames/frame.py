from typing import Optional, Self

from pybattle.ansi.colors import Color, Colors
from pybattle.debug.log import Logger
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Matrix, Cell
from pybattle.window.grid.range import RectRange
from pybattle.window.grid.size import Size


class Frame:
    """A empty box with a border.

    Get all box chars here: https://en.wikipedia.org/wiki/Box-drawing_character"""

    def __init__(
        self,
        size: Size | str,
        title: Optional[str] = None,
        border_color: Optional[Color] = None,
        title_color: Optional[Color] = None,
    ) -> None:
        if isinstance(size, str):
            self.size = Size(size)
        else:
            self.size = size
        self.contents = Matrix(self.inner_size)
        self.title = title
        
        if border_color is None:
            border_color = Colors.DEFAULT
        
        if title_color is None:
            title_color = Colors.DEFAULT
        
        self.border_color = border_color
        self.title_color = title_color
        
        self._update_frame()

    @property
    def width(self) -> int:
        return self.size.width

    @property
    def height(self) -> int:
        return self.size.height

    @property
    def inner_height(self) -> int:
        return self.inner_size.height

    @property
    def inner_width(self) -> int:
        return self.inner_size.width

    @property
    def inner_size(self) -> Size:
        return self.size - 2

    @property
    def icols(self) -> int:
        """Index columns."""
        return self.width - 1

    @property
    def irows(self) -> int:
        """Index rows."""
        return self.height - 1

    def _update_frame(self) -> None:
        if self.title is None:
            frame = f'╭{"─" * self.inner_width}╮\n'
        else:
            if self.inner_width - len(self.title) - 3 == 0:
                Logger.warning(f'Title is too long for size: {self.size}. May cause unintended problems.')

            # - 3 for  vv            v
            frame = f'╭─ {self.title} {"─" * (self.inner_width - len(self.title) - 3)}╮\n'

        for i in range(self.inner_height):
            new_line = '\n'
            frame += f'│{"".join([cell.value for cell in self.contents[i]]).rstrip(new_line)}│\n'

        frame += f'╰{"─" * self.inner_width}╯\n'

        colors = [(Coord(i, 1), Colors.DEFAULT) for i in range(1, self.irows)]
        colors += [(coord + 1, color) for coord, color in self.contents.colors]
        if self.border_color is not None:
            colors += [(Coord(i, 0), self.border_color) for i in range(self.height)]
            colors += [(Coord(i, self.width - 1), self.border_color) for i in range(self.height)]
        if self.title_color is not None and self.title is not None:
            colors += [(Coord(0, len(self.title)), self.border_color)]
            colors += [(Coord(0, 3), self.title_color)]
        
        self.matrix = Matrix(frame, *colors)

    def __getitem__(self, item) -> None:
        return self.matrix[item]

    def __setitem__(self, item, to) -> None:
        self.matrix[item] = to

    @property
    def top_edge_positions(self) -> RectRange:
        return RectRange(Coord(0, self.icols), Coord(0, 1))

    @property
    def bottom_edge_positions(self) -> RectRange:
        return RectRange(Coord(self.irows, self.icols), Coord(self.irows, 1))

    @property
    def left_edge_positions(self) -> RectRange:
        return RectRange(Coord(self.irows, 0), Coord(1, 0))

    @property
    def right_edge_positions(self) -> RectRange:
        return RectRange(Coord(self.irows, self.icols), Coord(1, self.icols))

    @property
    def top_left_corner(self) -> Coord:
        return Coord(0, 0)

    @property
    def bottom_left_corner(self) -> Coord:
        return Coord(self.irows, 0)

    @property
    def top_right_corner(self) -> Coord:
        return Coord(0, self.icols)

    @property
    def bottom_right_corner(self) -> Coord:
        return Coord(self.irows, self.icols)

    def __str__(self) -> str:
        return str(self.matrix)

    def add_frame(self, frame: "Frame", pos: Coord = Coord(0, 0)) -> None:
        # TODO: Fix corner going like this:
        # ╭──────────┬───────┬
        # │          ╰───────┤
        # ╰──────────────────╯
        top_left = pos
        top_right = pos + frame.top_right_corner
        bottom_left = pos + frame.bottom_left_corner
        bottom_right = pos + frame.bottom_right_corner

        Logger.info_debug(repr(frame.matrix))
        Logger.info_debug(repr(self.matrix[top_left: frame.size + pos - 1]))

        self.matrix[top_left: frame.size + pos - 1] = frame.matrix

        Logger.info_debug(repr(self.matrix))

        if top_left in self.top_edge_positions:
            self.matrix.change_cell_value(top_left, '┬')
        elif top_left in self.left_edge_positions:
            self.matrix.change_cell_value(top_left, '├')

        if top_right in self.top_edge_positions:
            self.matrix.change_cell_value(top_right, '┬')
        elif top_right in self.right_edge_positions:
            self.matrix.change_cell_value(top_right, '┤')

        if bottom_left in self.top_edge_positions:
            self.matrix.change_cell_value(bottom_left, '┴')
        elif bottom_left in self.left_edge_positions:
            self.matrix.change_cell_value(bottom_left, '├')

        if bottom_right in self.top_edge_positions:
            self.matrix.change_cell_value(bottom_right, '┴')
        elif bottom_right in self.right_edge_positions:
            self.matrix.change_cell_value(bottom_right, '┤')

        # Overlap Name
        if self.title is not None:
            for i, char in enumerate(' ' + self.title + ' '):
                self.matrix[Coord(0, i + 2)] = Cell(char, self.title_color)
        
        if self.title is not None:
            self.matrix.add_color(Coord(0, len(self.title) + 4), self.border_color)
        
        Logger.info_debug(repr(self.matrix))
