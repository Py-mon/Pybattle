from typing import Optional, Self

from numpy import full

from src.error import InsufficientArgumentsError, OutOfBoundsError
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
        self.contents = contents
        self.name = name
        self.name_location = name_location
        
        if size is not ...:
            self.size = Size.convert_reference(size)
            
            if self.contents is not None:
                if isinstance(contents, str):
                    self.contents = Matrix(contents)
                
                height = self.contents.size.height // 2
                width = self.contents.size.width // 2
                              
                middle_height = (self.size.height - 2) // 2
                middle_width = (self.size.width - 2) // 2
                
                array = full(self.size.subtract(2).reverse, ' ')
                
                starting_height = middle_height - height
                ending_height = middle_height + height
                if height == 0:
                    ending_height = middle_height + self.contents.size.height
                
                starting_width = middle_width - width
                ending_width = middle_width + width

                array[starting_height: ending_height,
                      starting_width: ending_width] = self.contents._matrix
                
                self.contents = Matrix.array_to_matrix(array)
                
        elif self.contents is not None:
            if isinstance(contents, str):
                self.contents = Matrix(contents)
            print(self.contents)
            self.size = self.contents.size + 2
            #self.size.height -= 1  # Cuts off the bottom without
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
    def icols(self):
        return self.width - 1

    @property
    def irows(self):
        return self.height - 1

    def _update_frame(self) -> None:
        frame = f'╭{"─" * (self.width - 2)}╮\n'
        for i in range(self.height - 2):
            if self.contents is None:
                frame += f'│{" " * (self.width - 2)}│\n'
            else:
                x = '\n'  # Doesn't allow "\" in f-strings
                frame += f'│{"".join(self.contents[i]).rstrip(x)}│\n'

        frame += f'╰{"─" * (self.width - 2)}╯\n'
        
        print(frame)

        self.matrix = Matrix(frame)
        
        if self.name is not None:
            for i, char in enumerate(' ' + self.name + ' '):
                try:
                    self.matrix[self.name_location.y, i + self.name_location.x] = char
                except IndexError:
                    raise Logger.error(f'Starting at {self.name_location.coords} the name: " {self.name} " is out of bounds of {self.size.size}', OutOfBoundsError)
                
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

    def add_frame(self, frame: Self, pos: CoordReference = Coord(0, 0)):
        pos = Coord.convert_reference(pos)

        # TODO: Fix Errors
        if pos.x + frame.width >= self.matrix.size.width:
            raise Logger.error(
                f'pos x: {pos.x} is out of bounds of {self.matrix.size.width - frame.width}', OutOfBoundsError)

        elif pos.y + frame.height >= self.matrix.size.height:
            raise Logger.error(
                f'pos y: {pos.y} is out of bounds of {self.matrix.size.height - frame.width}', OutOfBoundsError)

        top_left = pos
        top_right = pos + frame.top_right_corner
        bottom_left = pos + frame.bottom_left_corner
        bottom_right = pos + frame.bottom_right_corner

        print(frame.matrix._matrix)
        print(self.matrix[top_left.y: frame.height + pos.y,
                          top_left.x: frame.width + pos.x])

        self.matrix[top_left.y: frame.height + pos.y,
                    top_left.x: frame.width + pos.x] = frame.matrix._matrix

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
