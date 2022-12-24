from typing import Optional, Self

from pybattle.log import Logger
from pybattle.types_ import CoordReference, SizeReference
from pybattle.window.coord import Coord
from pybattle.window.matrix import Matrix
from pybattle.window.range import Range
from pybattle.window.size import Size


class Frame:
    """A empty box with a border.

    Get all box chars here: https://en.wikipedia.org/wiki/Box-drawing_character"""

    def __init__(
        self,
        size: SizeReference,
        title: Optional[str] = None,
    ) -> None:
        self.size = Size(size)
        self.contents = Matrix(self.inner_size)
        self.title = title

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
                Logger.warning(f'Title is too long for size: {self.size}.')

            # - 3 for  vv            v
            frame = f'╭─ {self.title} {"─" * (self.inner_width - len(self.title) - 3)}╮\n'

        for i in range(self.inner_height):
            new_line = '\n'
            frame += f'│{"".join(self.contents[i]).rstrip(new_line)}│\n'

        frame += f'╰{"─" * self.inner_width}╯\n'

        self.matrix = Matrix(frame)

    def __getitem__(self, item) -> None:
        return self.matrix[item]

    def __setitem__(self, item, to) -> None:
        self.matrix[item] = to

    @property
    def top_edge_positions(self) -> Range:
        return Range(Coord(0, self.icols), Coord(0, 1))

    @property
    def bottom_edge_positions(self) -> Range:
        return Range(Coord(self.irows, self.icols), Coord(self.irows, 1))

    @property
    def left_edge_positions(self) -> Range:
        return Range(Coord(self.irows, 0), Coord(1, 0))

    @property
    def right_edge_positions(self) -> Range:
        return Range(Coord(self.irows, self.icols), Coord(1, self.icols))

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

    def add_frame(self, frame: "Frame", pos: CoordReference = Coord(0, 0)):
        # TODO: Make colors work in adding frames

        pos = Coord(pos)

        top_left = pos
        top_right = pos + frame.top_right_corner
        bottom_left = pos + frame.bottom_left_corner
        bottom_right = pos + frame.bottom_right_corner

        print(repr(frame.matrix))
        print(repr(self.matrix[top_left: frame.size + 1]))

        self.matrix[top_left: frame.size + pos] = frame.matrix

        print(repr(self.matrix))

        # TODO: Fix corner going like this:
        # ╭──────────┬───────┬
        # │          ╰───────┤
        # ╰──────────────────╯

        if top_left in self.top_edge_positions:
            self.matrix[top_left] = '┬'
        elif top_left in self.left_edge_positions:
            self.matrix[top_left] = '├'

        if top_right in self.top_edge_positions:
            self.matrix[top_right] = '┬'
        elif top_right in self.right_edge_positions:
            self.matrix[top_right] = '┤'

        if bottom_left in self.top_edge_positions:
            self.matrix[bottom_left] = '┴'
        elif bottom_left in self.left_edge_positions:
            self.matrix[bottom_left] = '├'

        if bottom_right in self.top_edge_positions:
            self.matrix[bottom_right] = '┴'
        elif bottom_right in self.right_edge_positions:
            self.matrix[bottom_right] = '┤'

        # Overlaps Name
        if self.title is not None:
            for i, char in enumerate(' ' + self.title + ' '):
                self.matrix[i + 2, 0] = char

        print(self.matrix)
