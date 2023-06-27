from copy import copy
from typing import Any, Callable, Optional, Self

from pybattle.ansi.colors import Colors, ColorType
from pybattle.log.errors import SizeTooSmall
from pybattle.types_ import Align, Direction
from pybattle.window.frames.border.border_type import Borders, BorderType
from pybattle.window.frames.border.junction_table import get_junction
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Cell, Junction, Matrix
from pybattle.window.grid.range import center_range, rect_range, selection_range
from pybattle.window.grid.size import Size


class Frame:
    """Boxes to store information and events."""

    def __init__(
        self,
        contents: Matrix,
        title: Optional[str] = None,
        event: Optional[Callable[(...), Any]] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        base_color: ColorType = Colors.DEFAULT,
    ) -> None:
        self.event = event
        self.title = title
        self.border = border_type
        self.border_color = border_color
        self.title_color = title_color

        self.contents = contents
        self.size = self.contents.size + 2

        self.frames: list[tuple[Self, Coord]] = []
        self.changes: list[tuple] = []

        self.base_color: ColorType = base_color

        # self.update()

    @property
    def all_frames(self) -> list[Self]:
        """All of the Frames including this one"""
        return [frame for frame, _ in self.frames] + [self]

    def _reconstruct(self) -> None:
        """Reconstruct the border and contents for the Frame"""
        frame = []

        space = Cell(" ", collision=True)

        # Top Row
        if self.title:
            if self.size.inner.width - len(self.title) - 3 <= 0:
                raise SizeTooSmall(f"Frame of {self.size}", f"Title: '{self.title}'")

            title = [Cell(char) for char in self.title]  # was ()

            length_after_title = self.size.inner.width - len(self.title) - 3
            cells_after_title = self.border.horizontal_junction * length_after_title

            frame += [
                [
                    copy(self.border.top_right_junction),
                    copy(self.border.horizontal_junction),
                    space,
                    *title,
                    space,
                    *cells_after_title,
                    copy(self.border.top_left_junction),
                ]
            ]
        else:
            frame += [
                [
                    copy(self.border.top_right_junction),
                    *self.border.horizontal_junction * self.size.inner.width,
                    copy(self.border.top_left_junction),
                ]
            ]

        # Middle Contents
        for i in range(self.size.inner.height):
            cells = self.contents[i].cells
            frame += [
                [
                    copy(self.border.vertical_junction),
                    *cells,
                    copy(self.border.vertical_junction),
                ]
            ]

        # Bottom Row
        frame += [
            [
                copy(self.border.bottom_right_junction),
                *self.border.horizontal_junction * self.size.inner.width,
                copy(self.border.bottom_left_junction),
            ]
        ]

        self.matrix = Matrix(frame)

        if self.title:
            self.matrix[Coord(0, 2)].collision = True

    def _color(
        self,
        border_color: ColorType = ...,
        title_color: ColorType = ...,
        base_color: ColorType = ...,
    ) -> None:
        """Add border, title, and content colors"""
        self.matrix.colors = []

        if border_color is ...:
            border_color = self.border_color

        if title_color is ...:
            title_color = self.title_color

        if base_color is ...:
            base_color = self.base_color  # Clean ^ vv

        if base_color is not Colors.DEFAULT:
            self.matrix.color_all(base_color)

        self.matrix.color(
            border_color,
            rect_range(Coord(self.size.i.height, 0))
            + rect_range(
                Coord(self.size.i.height, self.size.i.width),
                Coord(self.size.i.height, 0),
            )
            + rect_range(
                Coord(self.size.i.height, self.size.i.width),
                Coord(0, self.size.i.width),
            )
            + rect_range(Coord(0, self.size.i.width)),
        )

        if self.title:
            self.matrix.color(
                title_color, rect_range(Coord(0, len(self.title) + 3), Coord(0, 3))
            )

    def update(
        self,
        border_color: ColorType = ...,
        title_color: ColorType = ...,
        base_color: ColorType = ...,
        frames: list[tuple[Self, Coord]] = ...,
    ) -> None:
        """Update the the Frame"""
        self._reconstruct()
        self._color(border_color, title_color, base_color)

        if frames is ...:
            frames = self.frames

        for frame, coord in frames.copy():
            self._add_frame(frame, coord)

        for item, to in self.changes.copy():
            self.matrix[item] = to

    def __getitem__(self, item) -> Cell:
        return self.matrix[item]

    def __setitem__(self, item, to) -> None:
        self.changes.append((item, to))

    @property
    def top_edges(self) -> list[Coord]:
        """```
         vvv
        ╭───╮
        │   │
        ╰───╯
        ```
        """
        return rect_range(Coord(0, self.size.inner.width), Coord(0, 1))

    @property
    def bottom_edges(self) -> list[Coord]:
        """```
        ╭───╮
        │   │
        ╰───╯
         ^^^
        ```
        """
        return rect_range(
            Coord(self.size.i.height, self.size.inner.width),
            Coord(self.size.i.height, 1),
        )

    @property
    def left_edges(self) -> list[Coord]:
        """```
         ╭───╮
        >│<  │
         ╰───╯
        ```
        """
        return rect_range(Coord(self.size.inner.height, 0), Coord(1, 0))

    @property
    def top_right_corner(self):
        return Coord(0, self.size.i.width)

    @property
    def right_edges(self) -> list[Coord]:
        """```
        ╭───╮
        │  >│<
        ╰───╯
        ```
        """
        return rect_range(
            Coord(self.size.inner.height, self.size.i.width),
            Coord(1, self.size.i.width),
        )

    @property
    def top_left_corner(self) -> Coord:
        """```
          v
        > ╭───╮
          │   │
          ╰───╯
        ```
        """
        return Coord(0, 0)

    @property
    def bottom_left_corner(self) -> Coord:
        """```
          ╭───╮
          │   │
        > ╰───╯
          ^
        ```
        """
        return Coord(self.size.i.height, 0)

    @property
    def bottom_right_corner(self) -> Coord:
        """
        ```
        ╭───╮
        │   │
        ╰───╯ <
            ^
        ```
        """
        return Coord(self.size.i.height, self.size.i.width)

    def __str__(self) -> str:
        return str(self.matrix)

    def _add_frame(self, frame: "Frame", pos: Coord = Coord(0, 0)) -> None:
        junctions: list[tuple[Junction, Coord]] = []
        for coord in frame.border_coords:
            coord_pos = coord + pos

            self_junction = self.matrix[coord_pos]
            frame_junction = frame.matrix[coord]

            if isinstance(self_junction, Junction) and isinstance(
                frame_junction, Junction
            ):
                junctions.append((self_junction + frame_junction, coord_pos))

        top_left = pos + frame.top_left_corner
        bottom_right = pos + frame.bottom_right_corner

        self.matrix[top_left:bottom_right] = frame.matrix

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
                    if not isinstance(self.matrix[ahead], Junction):
                        junction.dct.pop(direction)
                except IndexError:  # out of bounds
                    pass

            self.matrix[coord].dct = junction.dct

        if self.title is not None:
            for i, char in enumerate(" " + self.title + " "):
                self.matrix[Coord(0, i + 2)] = Cell(char, self.title_color)

            for i in range(len(self.title) + 4, self.size.inner.width):
                self.matrix[Coord(0, i)].color = self.border_color

    def add_frame(self, frame: "Frame", pos: Coord = Coord(0, 0)) -> None:
        """Add a Frame inside the Frame

        Automatically joins junctions"""
        self.frames.append((frame, pos))

    def remove_frame(self, frame: "Frame", pos: Coord = Coord(0, 0)) -> None:
        """Remove a Frame"""
        self.frames.remove((frame, pos))

    @classmethod
    def map(
        cls,
        contents: str,
        title: Optional[str] = None,
        event: Optional[Callable[[Self], Any]] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        base_color: ColorType = Colors.DEFAULT,
    ) -> Self:
        """
        Creates:
        ```
        ╭────────╮
        │abcdefgh│
        │ijklmnop│
        ╰────────╯
        """
        if not contents.endswith("\n"):
            contents += "\n"

        return cls(
            Matrix.from_str(contents),
            title,
            event,
            border_color,
            title_color,
            border_type,
            base_color,
        )

    @classmethod
    def box(
        cls,
        size: Size,
        title: Optional[str] = None,
        event: Optional[Callable[[Self], Any]] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        base_color: ColorType = Colors.DEFAULT,
    ) -> Self:
        """
        Creates:
        ```
        ╭──────╮
        │      │
        │      │
        ╰──────╯
        """
        matrix = cls(
            Matrix.from_size(size.inner),
            title,
            event,
            border_color,
            title_color,
            border_type,
            base_color,
        )
        # og_size = copy(matrix.size)
        matrix.size = size
        matrix.update()

        return matrix

    @property
    def border_coords(self):
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

    @classmethod
    def centered(
        cls,
        text: str,
        size: Size,
        title: Optional[str] = None,
        event: Optional[Callable[[Self], Any]] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        base_color: ColorType = Colors.DEFAULT,
        alignment: Align = Align.CENTER,
    ) -> Self:
        """
        Creates:
        ```
        ╭──────────╮
        │          │
        │  abcdef  │
        │   ghij   │
        │          │
        ╰──────────╯"""
        aligned_text = Matrix.from_str(text, align=alignment)
        slice_ = center_range(size.inner, aligned_text.size.i)

        contents = Matrix.from_size(size.inner)
        contents[slice_] = aligned_text

        return cls(
            contents, title, event, border_color, title_color, border_type, base_color
        )


# for _ in range(100):
#     f = Frame.box(Size(10, 25))
#     f.add_frame(Frame.box(Size(6, 7)))
#     f.add_frame(Frame.box(Size(5, 5)), Coord(4, 4))
    
#     f.update()
# print(f)