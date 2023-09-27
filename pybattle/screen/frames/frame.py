from copy import copy, deepcopy
from math import ceil
from typing import Any, Callable, Optional, Self

from pybattle.types_ import Alignment, Level

from pybattle.log.errors import AttributeMissing, TooSmallError
from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.border.border_type import Borders, BorderType
from pybattle.screen.frames.border.junction_table import get_junction
from pybattle.screen.grid.matrix import Cell, Junction, Grid
from pybattle.screen.grid.nested import level_out
from pybattle.screen.grid.point import Coord, Point, Size
from pybattle.types_ import Direction, JunctionDict
from dataclasses import dataclass


@dataclass
class Title:
    title: str
    x: int | Alignment = Alignment.LEFT
    color: Color = Colors.DEFAULT
    margin: int = 2
    level: Level = Level.TOP


def convert_align_to_pos(
    alignment: Alignment | int,
    of: "Size",
    right_adjustment: int = 0,
    margins: int = 3,
):
    if not isinstance(alignment, Alignment):
        return alignment

    if alignment == type(alignment).CENTER or alignment == type(alignment).MIDDLE:
        return of.center.x - 1
    elif alignment == type(alignment).LEFT:
        return margins
    elif alignment == type(alignment).RIGHT:
        return of.x - right_adjustment - margins
    return of.x


class Frame(Grid):
    @classmethod
    def centered(
        cls,
        text: str,
        size: Size,
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
        frame = cls(Cell.from_size(size), border_type)

        aligned_text = Grid(Cell.from_str(text), alignment)
        slice_ = get_box(frame.size, aligned_text.size.i)

        frame[slice_] = aligned_text

        return frame

    def __init__(
        self,
        cells: tuple[tuple[Cell, ...], ...],
        border_type: BorderType = Borders.THIN,
    ) -> None:
        super().__init__(cells)

        self.titles: list[Title] = []

        self.border_type = border_type
        self.border_color = None
        self.left_title_color = None
        self.right_title_color = None
        self.base_color = None

        self.border()

    def color_inner(self, color: Color):
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

        self.recolor_titles()

    def recolor_titles(self):
        for title in self.titles:
            pos = convert_align_to_pos(
                title.x, self.size, len(title.title), title.margin + 1
            )

            self.color(
                title.color,
                Coord(title.level.value, pos + len(title.title)).rect_range(
                    Coord(title.level.value, pos)
                ),
            )

    def unborder(self):
        """Remove the border."""
        self.cells = self[Coord(1, 1) : self.size.inner].cells

    def add_title(self, title: Title) -> None:
        matrix = Grid(Cell.from_str("╴" + title.title + "╶"))

        matrix.color(title.color, matrix.size.i.sub_x(1).rect_range(Coord(0, 1)))

        pos = convert_align_to_pos(
            title.x, self.size, len(title.title), title.margin + 1
        )
        print(title.x, pos)

        self[
            Coord(title.level.value, pos - 1) : Coord(
                title.level.value, pos + len(title.title)
            )
        ] = matrix

        self.titles.append(title)

    def border(self):
        """Add a border around the Matrix."""

        top_row = (
            self.border_type.top_right_junction,
            *(self.border_type.horizontal_junction * self.size.width),
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

        # for title in self.titles.copy():
        #     self.add_title(title)

        # matrix = Matrix(Cell.from_str("╴" + title.title + "╶"))
        # # matrix.color(color, matrix.size.i.rect_range(Coord(0, 1)))

        # pos = title.pos
        # if pos == Alignment.CENTER or pos == Alignment.MIDDLE:
        #     pos = Coord(0, self.size.center.x - 1)
        # elif pos == Alignment.LEFT:
        #     pos = Coord(0, 3)
        # elif pos == Alignment.RIGHT:
        #     pos = Coord(0, self.size.x - matrix.size.width - 1)

        # self[pos.add_x(-1) : Coord(pos.y, pos.x + len(title.title))] = matrix

        # self.color_titles()

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

        if not change_border_color and self.border_color is not None:
            self.color_border(self.border_color)

        # if self.title is not None:
        #     for i, char in enumerate(" " + self.title + " "):
        #         self[Coord(0, i + 2)] = Cell(char, self.title_color, True)


def get_box(center_of: Point, size: Point) -> slice:
    """Get a slice that is the size of inner_size in the center of the outer_size."""
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
