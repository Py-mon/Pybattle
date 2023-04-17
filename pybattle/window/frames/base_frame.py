from typing import Any, Callable, Optional, Self

from pybattle.ansi.colors import Colors, ColorType
from pybattle.debug.log import logger
from pybattle.debug.errors import InvalidSize
from pybattle.types_ import Direction
from pybattle.window.frames.border.border_type import Borders, BorderType, get_junction
from pybattle.window.grid.coord import Coord
from pybattle.window.grid.matrix import Cell, Matrix
from pybattle.window.grid.range import RectRange
from pybattle.window.grid.size import Size
from pybattle.types_ import ColorRange, Align


class _Frame:
    """The base class for creating boxes to store information and events.

    Use this class rather than Frame for inheriting."""

    def __init__(
        self,
        contents: Matrix,
        title: Optional[str] = None,
        event: Optional[Callable[[Self], Any]] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        colors: list[ColorRange] = [],
    ) -> None:
        self.event = event
        self.title = title
        self.border = border_type
        self.border_color = border_color
        self.title_color = title_color

        self.contents = contents
        self.size = self.contents.size + 2

        self.frames: list[tuple[Self, Coord]] = []

        self.contents.add_colors(*colors)
        self.update()

    @property
    def event_frames(self) -> list[Self]:
        """All of the non-static Frames (Frames with events)"""
        return [
            frame
            for frame, _ in self.frames + [(self, Coord(0, 0))]
            if frame.event is not None
        ]

    def _reconstruct(self) -> None:
        """Reconstruct the border and contents for the Frame"""
        frame = []

        space = Cell(" ")

        # Top Row
        if self.title:
            if self.size.inner.width - len(self.title) - 3 <= 0:
                raise InvalidSize(f"Title: '{self.title}'", f"Frame of {self.size}")

            title = (Cell(char) for char in self.title)

            length_after_title = self.size.inner.width - len(self.title) - 3
            cells_after_title = self.border.horizontal_cell * length_after_title

            frame += [
                [
                    self.border.top_right_cell,
                    self.border.horizontal_cell,
                    space,
                    *title,
                    space,
                    *cells_after_title,
                    self.border.top_left_cell,
                ]
            ]
        else:
            frame += [
                [
                    self.border.top_right_cell,
                    *self.border.horizontal_cell * self.size.inner.width,
                    self.border.top_left_cell,
                ]
            ]

        # Middle Contents
        for i in range(self.size.inner.height):
            cells = self.contents[i].cells
            frame += [
                [
                    self.border.vertical_cell,
                    *cells,
                    self.border.vertical_cell,
                ]
            ]

        # Bottom Row
        frame += [
            [
                self.border.bottom_right_cell,
                *self.border.horizontal_cell * self.size.inner.width,
                self.border.bottom_left_cell,
            ]
        ]

        self.matrix = Matrix(frame)

    def _color(
        self, border_color: ColorType = ..., title_color: ColorType = ...
    ) -> None:
        """Add border, title, and content colors"""
        self.matrix.colors = []

        if border_color is ...:
            border_color = self.border_color

        if title_color is ...:
            title_color = self.title_color

        self.matrix.add_colors(
            *((color, range_) for color, range_ in self.contents.colors)
        )

        self.matrix.add_colors(
            (border_color, RectRange(Coord(self.size.i.height, 0), Coord(0, 0))),
            (
                border_color,
                RectRange(
                    Coord(self.size.i.height, self.size.i.width),
                    Coord(self.size.i.height, 0),
                ),
            ),
            (
                border_color,
                RectRange(
                    Coord(self.size.i.height, self.size.i.width),
                    Coord(0, self.size.i.width),
                ),
            ),
            (border_color, RectRange(Coord(0, self.size.i.width), Coord(0, 0))),
        )

        if self.title:
            self.matrix.add_colors(
                (
                    title_color,
                    RectRange(Coord(0, len(self.title) + 3), Coord(0, 3)),
                )
            )

    def update(self) -> None:
        """Update the the Frame"""
        self._reconstruct()
        self._color()

        # for frame, coord in self.frames:
        #     self.add_frame(frame, coord)

    def __getitem__(self, item) -> None:
        return self.matrix[item]

    def __setitem__(self, item, to) -> None:
        self.matrix[item] = to

    @property
    def top_edges(self) -> RectRange:
        """```
         vvv
        ╭───╮
        │   │
        ╰───╯
        ```
        """
        return RectRange(Coord(0, self.size.inner.width), Coord(0, 1))

    @property
    def bottom_edges(self) -> RectRange:
        """```
        ╭───╮
        │   │
        ╰───╯
         ^^^
        ```
        """
        return RectRange(
            Coord(self.size.i.height, self.size.inner.width),
            Coord(self.size.i.height, 1),
        )

    @property
    def left_edges(self) -> RectRange:
        """```
         ╭───╮
        >│<  │
         ╰───╯
        ```
        """
        return RectRange(Coord(self.size.inner.height, 0), Coord(1, 0))

    @property
    def right_edges(self) -> RectRange:
        """```
        ╭───╮
        │  >│<
        ╰───╯
        ```
        """
        return RectRange(
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
    def top_right_corner(self) -> Coord:
        """
        ```
            v
        ╭───╮ <
        │   │
        ╰───╯
        ```
        """
        return Coord(0, self.size.i.width)

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

    @property
    def border_coords(self) -> list[Coord]:
        """All of the coordinates on the border"""
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

    def add_frame(self, frame: "_Frame", pos: Coord = Coord(0, 0)) -> None:
        """Add a Frame inside the Frame

        Automatically joins conjunctions"""

        self.frames.append((frame, pos))

        junctions = []
        for coord in frame.border_coords:
            coord_pos = coord + pos

            self_junction = self.matrix[coord_pos].junction
            frame_junction = frame.matrix[coord].junction
            if self_junction is not None and frame_junction is not None:
                junctions.append((self_junction | frame_junction, coord_pos))

        top_left = pos
        bottom_right = pos + frame.bottom_right_corner

        logger.debug(repr(self.matrix[top_left:bottom_right]))
        logger.debug(repr(frame.matrix))

        self.matrix[top_left:bottom_right] = frame.matrix

        logger.debug(repr(self.matrix))

        for junction, coord in junctions.copy():
            logger.debug(str((junction, coord)))

            for direction in junction.copy():
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
                    if not self.matrix[ahead].junction:
                        junction.pop(direction)
                except IndexError:
                    pass

            for thickness in junction.values():
                if thickness != None:
                    self.matrix[coord].value = get_junction(junction)
                    break

        if self.title is not None:
            for i, char in enumerate(" " + self.title + " "):
                self.matrix[Coord(0, i + 2)] = Cell(char, self.title_color)

            for i in range(len(self.title) + 4, self.size.inner.width):
                self.matrix[Coord(0, i)].color = self.border_color

        logger.debug(repr(self.matrix))


class Frame:
    """Frame Constructors."""

    @staticmethod
    def map(
        contents: str,
        title: Optional[str] = None,
        event: Optional[Callable[[_Frame], Any]] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        colors: list[ColorRange] = [],
    ) -> _Frame:
        return _Frame(
            Matrix.from_str(contents),
            title,
            event,
            border_color,
            title_color,
            border_type,
            colors,
        )

    @staticmethod
    def box(
        size: Size,
        title: Optional[str] = None,
        event: Optional[Callable[[_Frame], Any]] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        colors: list[ColorRange] = [],
    ) -> _Frame:
        if size.inner == Size(0, 0):
            raise ValueError(f"{size} is too small.")

        return _Frame(
            Matrix.from_size(size.inner),
            title,
            event,
            border_color,
            title_color,
            border_type,
            colors,
        )

    @staticmethod
    def centered(
        text: str,
        size: Size,
        title: Optional[str] = None,
        event: Optional[Callable[[_Frame], Any]] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        alignment: Align = Align.CENTER,
        colors: list[ColorRange] = [],
    ) -> _Frame:
        aligned_text = Matrix.from_str(text, alignment=alignment)
        center_range = RectRange.center_range(size.inner, aligned_text.size.i)

        contents = Matrix.from_size(size.inner)
        contents[center_range] = aligned_text

        return _Frame(
            contents, title, event, border_color, title_color, border_type, colors
        )

    @classmethod
    def selection(
        cls,
        label: str,
        size: Size,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType = Borders.THIN,
        alignment: Align = Align.CENTER,
        colors: list[ColorRange] = [],
    ) -> _Frame:
        return cls.centered(
            label,
            size,
            None,
            None,
            border_color,
            title_color,
            border_type,
            alignment,
            colors,
        )
