from copy import copy, deepcopy
from math import ceil
from typing import Any, Callable, Optional, Self

from types_ import Alignment

from pybattle.log.errors import AttributeMissing, TooSmallError
from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.border.border_type import Borders, BorderType
from pybattle.screen.frames.border.junction_table import get_junction
from pybattle.screen.grid.matrix import Cell, Junction, Matrix
from pybattle.screen.grid.nested import level_out
from pybattle.screen.grid.point import Coord, Point, Size
from pybattle.types_ import Alignment, Direction, JunctionDict


class Frame(Matrix):
    @classmethod
    def centered(
        cls,
        text: str,
        size: Size,
        title: Optional[str] = None,
        border_type: BorderType = Borders.THIN,
        alignment: Alignment = Alignment.CENTER,
    ) -> Self:
        """
        ```
        >>> Frame.centered("abcdef\\nghij")
        ╭──────────╮
        │          │
        │  abcdef  │
        │   ghij   │
        │          │
        ╰──────────╯
        """
        frame = cls(Cell.from_size(size), title, border_type)

        aligned_text = Matrix(Cell.from_str(text), alignment)
        slice_ = center_range(frame.size, aligned_text.size.i)

        # print(slice_)
        # print(repr(frame[slice_]))
        # print(repr(aligned_text))

        frame[slice_] = aligned_text

        return frame

    def __init__(
        self,
        cells: tuple[tuple[Cell, ...], ...],
        title: Optional[str] = None,
        border_type: BorderType = Borders.THIN,
    ) -> None:
        super().__init__(cells)

        self.title = title
        self.border_type = border_type

        self.border()

    def color_title(self, color: Color):
        self.title_color = color
        if self.title:
            self.color(color, Size(0, len(self.title) + 3).rect_range(Coord(0, 3)))
        else:
            raise AttributeMissing(f"color the title to '{color.name}'", "title")

    def color_inside(self, color: Color):
        self.base_color = color
        self.color(self.base_color, self.size.inner.rect_range(Coord(1, 1)))

    def color_border(self, color: Color):
        self.border_color = color
        self.color(
            self.border_color,
            Size(self.size.i.height, 0).rect_range()
            + Size(self.size.i.height, self.size.i.width).rect_range(
                Coord(self.size.i.height, 0)
            )
            + Size(self.size.i.height, self.size.i.width).rect_range(
                Coord(0, self.size.i.width)
            )
            + Size(0, self.size.i.width).rect_range(),
        )
        if self.title:
            self.color_title(self.title_color)

    def set_title(self, new_title: str):
        self.title = new_title
        self.reborder()

    def reborder(self):
        self.cells = self[Coord(1, 1) : self.size.inner].cells

        self.border()

    def border(self):
        """Add a border around the Matrix"""
        if self.title:
            if self.size.inner.width - len(self.title) - 3 <= 0:
                raise TooSmallError(f"Frame of {self.size}", f"Title: '{self.title}'")

            cell_title = [Cell(char) for char in self.title]  # was ()

            length_after_title = self.size.width - len(self.title) - 3
            cells_after_title = (
                self.border_type.horizontal_junction * length_after_title
            )

            top_row = (
                self.border_type.top_right_junction,
                self.border_type.horizontal_junction,
                Cell(" ", collision=True),
                *cell_title,
                Cell(" ", collision=True),
                *cells_after_title,
                self.border_type.top_left_junction,
            )

        else:
            top_row = (
                self.border_type.top_right_junction,  # all theses where copied
                *self.border_type.horizontal_junction * self.size.width,
                self.border_type.top_left_junction,
            )

        left_column = self.border_type.vertical_junction * self.size.height
        right_column = self.border_type.vertical_junction * self.size.height

        bottom_row = (
            self.border_type.bottom_right_junction,
            *self.border_type.horizontal_junction * self.size.width,
            self.border_type.bottom_left_junction,
        )

        self.extend_column(right_column)
        self.extend_column(left_column, -1)

        self.extend_row(top_row, -1)
        self.extend_row(bottom_row)

        self.border_coords = (
            Size(0, self.size.i.width).rect_range()
            + Size(self.size.i.height, self.size.i.width).rect_range(
                Coord(self.size.i.height, 0)
            )
            + Size(self.size.inner.height, 0).rect_range(Coord(1, 0))
            + Size(self.size.inner.height, self.size.i.width).rect_range(
                Coord(1, self.size.i.width)
            )
        )

    def add_frame(
        self,
        frame: "Frame",
        pos: Coord = Coord(0, 0),
        change_border_color: bool = False,
    ) -> None:
        # deepcopy frame if not wanted to share changes
        # frame.objs.append(self)

        junctions: list[tuple[Junction, Coord]] = []
        for coord in frame.border_coords:
            coord_pos = coord + pos

            self_junction = self[coord_pos]
            frame_junction = frame[coord]

            if isinstance(self_junction, Junction) and isinstance(
                frame_junction, Junction
            ):
                junctions.append((self_junction + frame_junction, coord_pos))

        self.overlay(frame, pos)

        for junction, coord in junctions:
            for direction in junction.dct.copy():
                ahead = Coord(0, 0)
                match direction:
                    case Direction.UP:
                        ahead = Coord(coord.y - 1, coord.x)
                    case Direction.DOWN:
                        ahead = Coord(coord.y + 1, coord.x)
                    case Direction.LEFT:
                        ahead = Coord(coord.y, coord.x - 1)
                    case Direction.RIGHT:
                        ahead = Coord(coord.y, coord.x + 1)
                try:
                    if not isinstance(self[ahead], Junction):
                        junction.dct.pop(direction)
                except IndexError:  # out of bounds
                    pass

            self[coord]._value = junction.dct

        if not change_border_color and hasattr(self, "border_color"):
            self.color_border(self.border_color)

        if self.title is not None:
            for i, char in enumerate(" " + self.title + " "):
                self[Coord(0, i + 2)] = Cell(char, self.title_color, True)


def center_range(center_of: Point, size: Point) -> slice:
    """Get a slice that is the size of inner_size in the center of the outer_size"""
    return slice(
        Coord(
            ceil((center_of.y - size.y) / 2 - 1),
            ceil((center_of.x - size.x) / 2 - 1),
        ),
        Coord(
            ceil((center_of.y + size.y) / 2 - 1),
            ceil((center_of.x + size.x) / 2 - 1),
        ),
    )


f = Frame(Cell.from_size(Size(5, 12)))

f.add_frame(Frame(Cell.from_size(Size(2, 5))))

print(f)
