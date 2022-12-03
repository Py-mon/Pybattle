"""A border around some contents."""

from typing import Optional

from src.log import Logger
from src.types_ import CoordReference, SizeReference
from src.window.coord import Coord, CoordList
from src.window.matrix import Matrix
from src.window.size import Size


class Frame:
    """A border around some contents.

    Get box chars here: https://en.wikipedia.org/wiki/Box-drawing_character"""

    def __init__(
        self,
        contents: Optional[str] | Matrix = None,
        size: SizeReference = ...,
        name: Optional[str] = None,
        name_location: Coord = Coord(2, 0)
    ) -> None:
        # TODO: Add centered contents

        self.contents = contents
        self.name = name
        self.name_location = name_location  # TODO: Make this do something

        if self.contents is not None:
            if size is not ...:
                Logger.info(f'Unused Frame size.', True)
            if isinstance(contents, str):
                self.contents = Matrix(contents)
            self.size = self.contents.size + 1
            self.size.height -= 1  # Cuts off the button without
        elif size is not ...:
            self.size = Size.convert_reference(size)
        else:
            raise ValueError(
                'Cannot have no contents and no size. Must have one.')

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
    def icols(self):
        return self.width - 1

    @property
    def irows(self):
        return self.height - 1

    def _update_frame(self) -> None:
        frame = f'╭{"─" * (self.width - 2)}╮\n'
        # frame = f'╭─ {self.name} {"─" * (self.width - 5 - len(self.name))}╮\n'
        for i in range(self.height - 2):
            if self.contents is None:
                frame += f'│{" " * (self.width - 2)}│\n'
            else:
                x = '\n'  # Doesn't allow "\" in f-strings
                print(i)
                frame += f'│{"".join(self.contents[i]).rstrip(x)}│\n'

        frame += f'╰{"─" * (self.width - 2)}╯\n'

        self.matrix = Matrix(frame)
        
        if self.name is not None:
            for i, char in enumerate(' ' + self.name + ' '):
                try:
                    self.matrix[self.name_location.y, i + self.name_location.x] = char
                except IndexError:
                    raise ValueError(f'Starting at {self.name_location.coords} the name: " {self.name} " is out of bounds of {self.size.size}')
                
    def __getitem__(self, item) -> None:
        return self.matrix[item]

    def __setitem__(self, item, to) -> None:
        self.matrix[item] = to

    @property
    def top_edge_positions(self) -> list[Coord]:
        return CoordList(Coord(1, 0), (Coord(self.icols, 0))).get_range()

    @property
    def bottom_edge_positions(self) -> list[Coord]:
        return CoordList(Coord(1, self.irows), (Coord(self.icols, self.irows))).get_range()

    @property
    def left_edge_positions(self) -> list[Coord]:
        return CoordList(Coord(0, 1), (Coord(0, self.irows))).get_range()

    @property
    def right_edge_positions(self) -> list[Coord]:
        return CoordList(Coord(self.icols, 1), (Coord(self.icols, self.irows))).get_range()

    @property
    def top_left_corner(self) -> Coord:
        return Coord(0, 0)

    @property
    def bottom_left_corner(self) -> Coord:
        return Coord(0, self.irows)

    @property
    def top_right_corner(self) -> Coord:
        return Coord(self.icols, 0)

    @property
    def bottom_right_corner(self) -> Coord:
        return Coord(self.icols, self.irows)

    def add_frame(
        self,
        frame: "Frame",  # Only Frames can be added not subclasses (not Self)
        pos: CoordReference = Coord(0, 0),
    ) -> None:
        # TODO: Not give error when out of bounds
        # TODO: Test out ansi escape code version with new matrix

        pos = Coord.convert_reference(pos)

        out_of_boundaries_step_x = (
            self.top_right_corner - (pos + frame.size.size)).x
        out_of_boundaries_step_y = (
            self.bottom_left_corner - (pos + frame.size.size)).y

        if out_of_boundaries_step_x <= 0:
            limit = 1 if out_of_boundaries_step_x < 0 else abs(
                out_of_boundaries_step_x)
            frame.width -= limit

        if out_of_boundaries_step_y <= 0:
            limit = 1 if out_of_boundaries_step_y < 0 else abs(
                out_of_boundaries_step_y)
            frame.height -= limit

        top_left = pos
        top_right = pos + frame.top_right_corner
        bottom_left = pos + frame.bottom_left_corner
        bottom_right = pos + frame.bottom_right_corner

        if self.top_edge_positions in top_left:
            self.matrix[*top_left.reverse] = '┬'
        elif self.left_edge_positions in top_left:
            self.matrix[*top_left.reverse] = '├'

        if self.top_edge_positions in top_right:
            self.matrix[*top_right.reverse] = '┬'
        elif self.right_edge_positions in top_right:
            self.matrix[*top_right.reverse] = '┤'

        if self.bottom_edge_positions in bottom_left:
            self.matrix[*bottom_left.reverse] = '┴'
        elif self.left_edge_positions in bottom_left:
            self.matrix[*bottom_left.reverse] = '├'

        if self.bottom_edge_positions in bottom_right:
            self.matrix[*bottom_right.reverse] = '┴'
        if self.right_edge_positions in bottom_right:
            self.matrix[*bottom_right.reverse] = '┤'

        frame_slice = frame[
            0: pos.y + frame.height,
            0: pos.x + frame.width
        ]

        for y in range(0, frame.height):
            for x in range(0, frame.width):
                if self.matrix[y + pos.y, x + pos.x] == ' ':
                    self.matrix[y + pos.y, x + pos.x] = frame_slice[y, x]

        print(Matrix.convert_array(self.matrix))


class Window(Frame):
    """The main border screen."""

    def add_frame(self, frame, pos):
        pos = Coord.convert_reference(pos)

        if pos.x + frame.width >= self.matrix.size.width:
            raise ValueError(
                f'pos x: {pos.x} is out of bounds of {self.matrix.size.width - frame.width}')

        elif pos.y + frame.height >= self.matrix.size.height:
            raise ValueError(
                f'pos y: {pos.y} is out of bounds of {self.matrix.size.height - frame.width}')

        top_left = pos
        top_right = pos + frame.top_right_corner
        bottom_left = pos + frame.bottom_left_corner
        bottom_right = pos + frame.bottom_right_corner

        # Removes the last column (which is only newlines)
        frame_without_newlines = frame.matrix._matrix[:, :-1]

        print(frame.matrix._matrix[:, :-1])
        print(self.matrix[top_left.y: frame_without_newlines.shape[0] + pos.y,
                          top_left.x: frame_without_newlines.shape[1] + pos.x])

        self.matrix[top_left.y: frame_without_newlines.shape[0] + pos.y,
                    top_left.x: frame_without_newlines.shape[1] + pos.x] = frame.matrix._matrix[:, :-1]

        print(self.matrix)

        # TODO: Fix corner going like this:
        # ╭──────────┬───────┬
        # │          ╰───────┤
        # ╰──────────────────╯

        if top_left in self.top_edge_positions:
            self.matrix[top_left.reverse] = '┬'
        elif top_left in self.left_edge_positions:
            self.matrix[top_left.reverse] = '├'

        if top_right in self.top_edge_positions:
            self.matrix[top_right.reverse] = '┬'
        elif top_right in self.right_edge_positions:
            self.matrix[top_right.reverse] = '┤'

        if bottom_left in self.top_edge_positions:
            self.matrix[bottom_left.reverse] = '┴'
        elif bottom_left in self.left_edge_positions:
            self.matrix[bottom_left.reverse] = '├'

        if bottom_right in self.top_edge_positions:
            self.matrix[bottom_right.reverse] = '┴'
        elif bottom_right in self.right_edge_positions:
            self.matrix[bottom_right.reverse] = '┤'

        # Overlaps Name
        if self.name is not None:
            for i, char in enumerate(' ' + self.name + ' '):
                self.matrix[self.name_location.y, i + self.name_location.x] = char

        print(self.matrix)
