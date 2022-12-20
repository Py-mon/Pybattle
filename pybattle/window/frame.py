from typing import Optional, Self

from pybattle.error import InsufficientArgumentsError
from pybattle.log import Logger
from pybattle.types_ import CoordReference, SizeReference
from pybattle.window.coord import Coord
from pybattle.window.matrix import Matrix, ColorCoord
from pybattle.window.range import Range
from pybattle.window.size import Size
from pybattle.ansi.color import Colors

class Frame:
    """A border around some contents.

    Get box chars here: https://en.wikipedia.org/wiki/Box-drawing_character"""

    def __init__(
        self,
        contents: Optional[str] | Matrix = None,
        size: SizeReference = ...,
        name: Optional[str] = None,
    ) -> None:
        self.contents = contents
        self.name = name
        self.colors = []
        
        if size is not ...:
            self.size = Size.convert_reference(size)

            if self.contents is not None:
                if isinstance(contents, str):
                    self.contents = Matrix(contents)

                matrix = Matrix([[' ' for _ in range(self.inner_width)]
                               for _ in range(self.inner_height)])

                print(repr(matrix))

                text_center = self.contents.size.center

                inner_frame_center = self.inner_size.center

                starting = inner_frame_center - text_center
                ending = inner_frame_center + text_center

                print(text_center, text_center)
                print(inner_frame_center, inner_frame_center)
                print(starting, ending)
                print()
                print(repr(matrix[starting: ending]))
                print(repr(self.contents))

                matrix[starting: ending] = self.contents

                self.contents = matrix

        elif self.contents is not None:
            if isinstance(contents, str):
                self.contents = Matrix(contents)
            self.size = self.contents.size + 2
        else:
            raise Logger.error(
                'Cannot have no contents and no size. Must have at least one.', InsufficientArgumentsError)
            
        self._update_frame()

    @property
    def width(self) -> int:
        return self.size.width

    @width.setter
    def width(self, to: int):
        self.size.width = to
        self._update_frame()

    @property
    def height(self) -> int:
        return self.size.height

    @height.setter
    def height(self, to: int):
        self.size.height = to
        self._update_frame()

    @property
    def inner_height(self) -> int:
        return self.height - 2

    @property
    def inner_width(self) -> int:
        return self.width - 2

    @property
    def inner_size(self) -> Size:
        return self.size - 2

    @property
    def icols(self) -> int:
        return self.width - 1

    @property
    def irows(self) -> int:
        return self.height - 1

    def _update_frame(self) -> None:
        if self.name is None:
            frame = f'╭{"─" * self.inner_width}╮\n'
        else:
            frame = f'╭─ {self.name} {"─" * (self.inner_width - len(self.name) - 3)}╮\n'
        for i in range(self.inner_height):
            if self.contents is None:
                frame += f'│{" " * self.inner_width}│\n'
            else:
                x = '\n'  # Doesn't allow "\" in f-strings
                frame += f'│{"".join(self.contents[i]).rstrip(x)}│\n'

        frame += f'╰{"─" * self.inner_width}╯\n'

        if self.colors:
            self.matrix = Matrix(frame, *self.colors)
        else:
            self.matrix = Matrix(frame)
            
    def __getitem__(self, item) -> None:
        return self.matrix[item]

    def __setitem__(self, item, to) -> None:
        self.matrix[item] = to

    @property
    def top_edge_positions(self) -> Range:
        print(Coord(0, self.icols), Coord(1, 1))
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

    def add_frame(self, frame: Self, pos: CoordReference = Coord(0, 0)):
        # TODO: Make colors work change in adding frames
        
        pos = Coord.convert_reference(pos)

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
        if self.name is not None:
            for i, char in enumerate(' ' + self.name + ' '):
                self.matrix[i + 2, 0] = char
        
        print(self.matrix)
