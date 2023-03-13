from typing import Optional, Self

from pybattle.ansi.colors import ColorType, Colors
from pybattle.debug.log import Logger
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Matrix, Cell
from pybattle.window.grid.range import RectRange
from pybattle.window.grid.size import Size
from pybattle.window.frames.border_type import Borders, BorderType
from pybattle.window.frames.conjunctions import get_conjunction, Conjunction


class Frame:
    """A empty box with a border. """

    def __init__(
        self,
        size: Size,
        title: Optional[str] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
    ) -> None:
        self.size = size
        self.contents = Matrix(self.inner_size)
        self.title = title

        self.border = border_type

        self.border_color = border_color
        self.title_color = title_color

        self.frames: list[tuple[Self, Coord]] = []

        self._construct_frame()

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
        return self.width - 1

    @property
    def irows(self) -> int:
        return self.height - 1

    def _create_frame(self) -> None:
        # frame = ''

        # border = self.border

        # if self.title:
        #     if self.inner_width - len(self.title) - 3 == 0:
        #         Logger.error(f'Title is too big for size: {self.size}.')

        #     frame += f'{border.top_right_cell}{border.horizontal_cell} {self.title} {border.horizontal_cell * (self.inner_width - len(self.title) - 3)}{self.border.top_left_cell}\n'
        # else:
        #     frame += f'{border.top_right_cell}{border.horizontal_cell * self.inner_width}{self.border.top_left_cell}\n'

        # for i in range(self.inner_height):
        #     new_line = '\n'
        #     frame += f'{border.vertical_cell}{"".join([cell.value for cell in self.contents[i]]).rstrip(new_line)}{border.vertical_cell}\n'

        # frame += f'{border.bottom_right_cell}{border.horizontal_cell * self.inner_width}{border.bottom_left_cell}\n'

        # self.matrix = Matrix(frame)

        frame = []

        border = self.border

        space = Cell(' ')

        length = border.horizontal_cell * self.inner_width
        
        if self.title:
            if self.inner_width - len(self.title) - 3 == 0:
                Logger.error(f'Title is too big for size: {self.size}.')

            title = (Cell(char) for char in self.title)

            length_after_title = (self.inner_width - len(self.title) - 3)
            cells_after_title = border.horizontal_cell * length_after_title

            frame += [[
                border.top_right_cell, border.horizontal_cell, space, *
                title, space, *cells_after_title, border.top_left_cell,
            ]]
        else:
            frame += [[
                border.top_right_cell, *length, self.border.top_left_cell,
            ]]

        # Middle
        for i in range(self.inner_height):
            cells = (cell for cell in self.contents[i])
            frame += [[
                border.vertical_cell, *cells, border.vertical_cell,
            ]]

        frame += [[
            border.bottom_right_cell, *length, border.bottom_left_cell
        ]]

        self.matrix = Matrix(frame)

    def _color_frame(self) -> None:
        content_colors = [(coord + 1, color)
                          for coord, color in self.contents.colors]

        border_colors = [(Coord(i, 0), self.border_color) for i in range(self.height)] \
            + [(Coord(i + 1, 1), Colors.DEFAULT) for i in range(self.inner_height)] \
            + [(Coord(i, self.width - 1), self.border_color)
                for i in range(self.height)]

        title_colors = []
        if self.title:
            title_colors = [(Coord(0, 3), self.title_color)] \
                + [(Coord(0, len(self.title) + 3), self.border_color)]

        self.matrix.add_colors(*content_colors, *border_colors, *title_colors)

    def _construct_frame(self) -> None:
        self._create_frame()
        self._color_frame()

    def __getitem__(self, item) -> None:
        return self.matrix[item]

    def __setitem__(self, item, to) -> None:
        self.matrix[item] = to

    @property
    def top_edges(self) -> RectRange:
        return RectRange(Coord(0, self.inner_width), Coord(0, 1))

    @property
    def bottom_edges(self) -> RectRange:
        return RectRange(Coord(self.irows, self.inner_width), Coord(self.irows, 1))

    @property
    def left_edges(self) -> RectRange:
        return RectRange(Coord(self.inner_height, 0), Coord(1, 0))

    @property
    def right_edges(self) -> RectRange:
        return RectRange(Coord(self.inner_height, self.icols), Coord(1, self.icols))

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

    @property
    def border_coords(self) -> list[Coord]:
        return [
            *self.top_edges,
            *self.bottom_edges,
            *self.right_edges,
            *self.left_edges,
            self.bottom_left_corner,
            self.bottom_right_corner,
            self.top_right_corner,
            self.top_left_corner,
        ]

    def __str__(self) -> str:
        return str(self.matrix)
    
    def add_frame(self, frame: "Frame", pos: Coord = Coord(0, 0)) -> None:
        conjunctions = []
        for coord in frame.border_coords:
            coord_pos = coord + pos
            
            if self.matrix[coord_pos].conjunction:
                if coord_pos == Coord(0, 12):
                    print(self.matrix[coord_pos].conjunction | frame.matrix[coord].conjunction)
                conjunctions.append((self.matrix[coord_pos].conjunction | frame.matrix[coord].conjunction, coord_pos))
                
        top_left = pos
        bottom_right = pos + frame.bottom_right_corner

        self.matrix[top_left: bottom_right] = frame.matrix

        if self.title is not None:
            for i, char in enumerate(' ' + self.title + ' '):
                self.matrix[Coord(0, i + 2)] = Cell(char, self.title_color)

        if self.title is not None:
            self.matrix.add_color(
                Coord(0, len(self.title) + 4), self.border_color)
            
        for conjunction, coord in conjunctions:
            if coord == Coord(0, 12):
                print(conjunction)
            for direction in conjunction.copy():
                if direction == 'up':
                    ahead = Coord(coord.y - 1, coord.x)
                elif direction == 'down':
                    ahead = Coord(coord.y + 1, coord.x)
                elif direction == 'left':
                    ahead = Coord(coord.y, coord.x - 1)
                elif direction == 'right':
                    ahead = Coord(coord.y, coord.x + 1)
                try:
                    if not self.matrix[ahead].conjunction:
                        conjunction.pop(direction)
                except IndexError:
                    pass
            if coord == Coord(0, 12):
                print(coord, get_conjunction(conjunction))

            self.matrix[coord].value = get_conjunction(conjunction)

    @property
    def center(self):
        return self.size.center
