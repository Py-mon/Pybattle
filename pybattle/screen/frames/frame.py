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

# from pybattle.screen.window import Event
# from pybattle.screen.window import Event
from pybattle.types_ import Alignment, Direction, JunctionDict


class Event:
    pass


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

        print(slice_)
        print(repr(frame[slice_]))
        print(repr(aligned_text))

        frame[slice_] = aligned_text

        return frame

    def __init__(
        self,
        cells: list[list[Cell]],
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

    def reborder(self):
        self.cells = self.cells[1:-1]
        for row in self.cells:
            row.pop(0)
            row.pop(-1)

        self.recache()

        self.border()
        
    def recache(self):
        super().__init__(self.cells)

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

            top_row = [
                self.border_type.top_right_junction,
                self.border_type.horizontal_junction,
                Cell(" ", collision=True),
                *cell_title,
                Cell(" ", collision=True),
                *cells_after_title,
                self.border_type.top_left_junction,
            ]

        else:
            top_row = [
                self.border_type.top_right_junction,  # all theses where copied
                *self.border_type.horizontal_junction * self.size.width,
                self.border_type.top_left_junction,
            ]

        left_column = self.border_type.vertical_junction * self.size.height
        right_column = self.border_type.vertical_junction * self.size.height

        bottom_row = [
            self.border_type.bottom_right_junction,
            *self.border_type.horizontal_junction * self.size.width,
            self.border_type.bottom_left_junction,
        ]
        self.extend_column()
        self.extend_column(-1)

        for i, cell in enumerate(left_column):
            self.cells[i][0] = cell

        for i, cell in enumerate(right_column):
            self.cells[i][-1] = cell

        self.extend_row(-1)
        self.extend_row()

        for i, cell in enumerate(top_row):
            print(cell)
            self.cells[0][i] = cell

        for i, cell in enumerate(bottom_row):
            self.cells[-1][i] = cell

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

            self[coord, "value"] = junction.dct

        if change_border_color:
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


# z = f.border_coords

# x = (
#     Size(0, f.size.i.width).rect_range()  # v
#     + Size(f.size.i.height, f.size.i.width).rect_range(Coord(f.size.i.height, 0))
#     + Size(f.size.inner.height, 0).rect_range(Coord(1, 0))
#     + Size(f.size.inner.height, f.size.i.width).rect_range(Coord(1, f.size.i.width))
# )


# class Frame:
#     """Boxes to store information. (Can be updated on frames with events)"""

#     def __init__(
#         self,
#         contents: Matrix,
#         title: Optional[str] = None,
#         events: Optional[list[Event]] = None,
#         border_color: Color = Colors.DEFAULT,
#         title_color: Color = Colors.DEFAULT,
#         border_type: BorderType = Borders.THIN,
#         base_color: Color = Colors.DEFAULT,
#     ) -> None:
#         self.events = events
#         if self.events is None:
#             self.events = []

#         self.title = title
#         self.border = border_type
#         self.border_color = border_color
#         self.title_color = title_color

#         self.contents = contents
#         self.size = self.contents.size + 2

#         self.frames: list[tuple[Self, Coord]] = []
#         self.changes: list[tuple] = []

#         self.base_color: Color = base_color

#         # self.update()

#         # self.scene = Scene(lambda: str(self), pos=Coord(0, 0))

#     @property
#     def all_frames(self) -> list[Self]:
#         """All of the Frames including this one"""
#         return [frame for frame, _ in self.frames] + [self]

#     def _reconstruct(self) -> None:
#         """Reconstruct the border and contents for the Frame"""
#         frame = []

#         space = Cell(" ", collision=True)

#         # Top Row
#         if self.title:
#             if self.size.inner.width - len(self.title) - 3 <= 0:
#                 raise TooSmallError(f"Frame of {self.size}", f"Title: '{self.title}'")

#             title = [Cell(char) for char in self.title]  # was ()

#             length_after_title = self.size.inner.width - len(self.title) - 3
#             cells_after_title = self.border.horizontal_junction * length_after_title

#             frame += [
#                 [
#                     copy(self.border.top_right_junction),
#                     copy(self.border.horizontal_junction),
#                     space,
#                     *title,
#                     space,
#                     *cells_after_title,
#                     copy(self.border.top_left_junction),
#                 ]
#             ]
#         else:
#             frame += [
#                 [
#                     copy(self.border.top_right_junction),
#                     *self.border.horizontal_junction * self.size.inner.width,
#                     copy(self.border.top_left_junction),
#                 ]
#             ]

#         # Middle Contents
#         for i in range(self.size.inner.height):
#             cells = self.contents[i].cells[0]
#             frame += [
#                 [
#                     copy(self.border.vertical_junction),
#                     *cells,
#                     copy(self.border.vertical_junction),
#                 ]
#             ]

#         # Bottom Row
#         frame += [
#             [
#                 copy(self.border.bottom_right_junction),
#                 *self.border.horizontal_junction * self.size.inner.width,
#                 copy(self.border.bottom_left_junction),
#             ]
#         ]

#         self.matrix = Matrix(frame)

#         if self.title:
#             self.matrix[Coord(0, 2)].collision = True

#     def _color(
#         self,
#         border_color: Color = ...,
#         title_color: Color = ...,
#         base_color: Color = ...,
#     ) -> None:
#         """Add border, title, and content colors"""
#         if border_color is ...:
#             border_color = self.border_color

#         if title_color is ...:
#             title_color = self.title_color

#         if base_color is ...:
#             base_color = self.base_color  # Clean ^ vv

#         if base_color is not Colors.DEFAULT:
#             self.matrix.color_all(base_color)

#         self.matrix.color(
#             border_color,
#             Size(self.size.i.height, 0).rect_range()
#             + Size(self.size.i.height, self.size.i.width).rect_range(
#                 Coord(self.size.i.height, 0)
#             )
#             + Size(self.size.i.height, self.size.i.width).rect_range(
#                 Coord(0, self.size.i.width)
#             )
#             + Size(0, self.size.i.width).rect_range(),
#         )

#         if self.title:
#             self.matrix.color(
#                 title_color, Size(0, len(self.title) + 3).rect_range(Coord(0, 3))
#             )

#     def update(
#         self,
#         border_color: Color = ...,
#         title_color: Color = ...,
#         base_color: Color = ...,
#         frames: list[tuple[Self, Coord]] = ...,
#     ) -> None:
#         """Update the the Frame"""
#         self._reconstruct()
#         self._color(border_color, title_color, base_color)

#         if frames is ...:
#             frames = self.frames

#         for frame, coord in frames.copy():
#             frame.update()
#             self._add_frame(frame, coord)

#         for item, to in self.changes.copy():
#             self.matrix[item] = to

#     def __getitem__(self, item) -> Cell:
#         return self.matrix[item]

#     def __setitem__(self, item, to) -> None:
#         self.changes.append((item, to))

#     @property
#     def top_edges(self) -> list[Coord]:
#         """```
#          vvv
#         ╭───╮
#         │   │
#         ╰───╯
#         ```
#         """
#         return Size(0, self.size.inner.width).rect_range(Coord(0, 1))

#     @property
#     def bottom_edges(self) -> list[Coord]:
#         """```
#         ╭───╮
#         │   │
#         ╰───╯
#          ^^^
#         ```
#         """
#         return Size(self.size.i.height, self.size.inner.width).rect_range(
#             Coord(self.size.i.height, 1),
#         )

#     @property
#     def left_edges(self) -> list[Coord]:
#         """```
#          ╭───╮
#         >│<  │
#          ╰───╯
#         ```
#         """
#         return Size(self.size.inner.height, 0).rect_range(Coord(1, 0))

#     @property
#     def top_right_corner(self):
#         return Coord(0, self.size.i.width)

#     @property
#     def right_edges(self) -> list[Coord]:
#         """```
#         ╭───╮
#         │  >│<
#         ╰───╯
#         ```
#         """
#         return Size(self.size.inner.height, self.size.i.width).rect_range(
#             Coord(1, self.size.i.width),
#         )

#     @property
#     def top_left_corner(self) -> Coord:
#         """```
#           v
#         > ╭───╮
#           │   │
#           ╰───╯
#         ```
#         """
#         return Coord(0, 0)

#     @property
#     def bottom_left_corner(self) -> Coord:
#         """```
#           ╭───╮
#           │   │
#         > ╰───╯
#           ^
#         ```
#         """
#         return Coord(self.size.i.height, 0)

#     @property
#     def bottom_right_corner(self) -> Coord:
#         """
#         ```
#         ╭───╮
#         │   │
#         ╰───╯ <
#             ^
#         ```
#         """
#         return Coord(self.size.i.height, self.size.i.width)

#     def __str__(self) -> str:
#         return str(self.matrix)

#     def __repr__(self) -> str:
#         return str(self.size)

#     def _add_frame(self, frame: "Frame", pos: Coord = Coord(0, 0)) -> None:
#         junctions: list[tuple[Junction, Coord]] = []
#         for coord in frame.border_coords:
#             coord_pos = coord + pos

#             self_junction = self.matrix[coord_pos]
#             frame_junction = frame.matrix[coord]

#             if isinstance(self_junction, Junction) and isinstance(
#                 frame_junction, Junction
#             ):
#                 junctions.append((self_junction + frame_junction, coord_pos))

#         top_left = pos + frame.top_left_corner
#         bottom_right = pos + frame.bottom_right_corner

#         self.matrix[top_left:bottom_right] = frame.matrix

#         for junction, coord in junctions:
#             for direction in junction.dct.copy():
#                 ahead = Coord(0, 0)
#                 match direction:
#                     case Direction.UP:
#                         ahead = Coord(coord.y - 1, coord.x)
#                     case Direction.DOWN:
#                         ahead = Coord(coord.y + 1, coord.x)
#                     case Direction.LEFT:
#                         ahead = Coord(coord.y, coord.x - 1)
#                     case Direction.RIGHT:
#                         ahead = Coord(coord.y, coord.x + 1)
#                 try:
#                     if not isinstance(self.matrix[ahead], Junction):
#                         junction.dct.pop(direction)
#                 except IndexError:  # out of bounds
#                     pass

#             frame_corner: Junction = self.matrix[coord]  # type: ignore
#             frame_corner.dct = junction.dct

#         if self.title is not None:
#             for i, char in enumerate(" " + self.title + " "):
#                 self.matrix[Coord(0, i + 2)] = Cell(char, self.title_color)

#             for i in range(len(self.title) + 4, self.size.inner.width):
#                 self.matrix[Coord(0, i)].color = self.border_color

#     def add_frame(self, frame: "Frame", pos: Coord = Coord(0, 0)) -> None:
#         """
#         Add a Frame inside the Frame

#         Joins Junctions together
#         """
#         self.frames.append((frame, pos))

#     def remove_frame(self, frame: "Frame", pos: Coord = Coord(0, 0)) -> None:
#         """Remove a Frame"""
#         self.frames.remove((frame, pos))

#     @classmethod
#     def map(
#         cls,
#         contents: str,
#         title: Optional[str] = None,
#         events: Optional[list[Event]] = None,
#         border_color: Color = Colors.DEFAULT,
#         title_color: Color = Colors.DEFAULT,
#         border_type: BorderType = Borders.THIN,
#         base_color: Color = Colors.DEFAULT,
#     ) -> Self:
#         """
#         ```
#         >>> Frame.box('abcdefgh\\nijklmnop')
#         ╭────────╮
#         │abcdefgh│
#         │ijklmnop│
#         ╰────────╯
#         ```
#         If one line is longer than another one, it expands the border.
#         """
#         if not contents.endswith("\n"):
#             contents += "\n"

#         return cls(
#             Matrix.from_str(contents),
#             title,
#             events,
#             border_color,
#             title_color,
#             border_type,
#             base_color,
#         )

#     @classmethod
#     def box(
#         cls,
#         size: Size,
#         title: Optional[str] = None,
#         events: Optional[list[Event]] = None,
#         border_color: Color = Colors.DEFAULT,
#         title_color: Color = Colors.DEFAULT,
#         border_type: BorderType = Borders.THIN,
#         base_color: Color = Colors.DEFAULT,
#     ) -> Self:
#         """
#         ```
#         >>> Frame.box(Size(4, 8))
#         ╭──────╮
#         │      │
#         │      │
#         ╰──────╯
#         """
#         matrix = cls(
#             Matrix.from_size(size.inner),
#             title,
#             events,
#             border_color,
#             title_color,
#             border_type,
#             base_color,
#         )
#         # og_size = copy(matrix.size)
#         matrix.size = size
#         matrix.update()

#         return matrix

#     @property
#     def border_coords(self):
#         return [
#             *self.top_edges,
#             *self.bottom_edges,
#             *self.right_edges,
#             *self.left_edges,
#             self.bottom_left_corner,
#             self.bottom_right_corner,
#             self.top_right_corner,
#             self.top_left_corner,
#         ]

#     @classmethod
#     def centered(
#         cls,
#         text: str,
#         size: Size,
#         title: Optional[str] = None,
#         events: Optional[list[Event]] = None,
#         border_color: Color = Colors.DEFAULT,
#         title_color: Color = Colors.DEFAULT,
#         border_type: BorderType = Borders.THIN,
#         base_color: Color = Colors.DEFAULT,
#         alignment: Align = Align.CENTER,
#     ) -> Self:
#         """
#         ```
#         >>> Frame.centered("abcdef\\nghij")
#         ╭──────────╮
#         │          │
#         │  abcdef  │
#         │   ghij   │
#         │          │
#         ╰──────────╯
#         """
#         aligned_text = Matrix.from_str(text, align=alignment)
#         slice_ = center_range(size.inner, aligned_text.size.i)

#         contents = Matrix.from_size(size.inner)
#         contents[slice_] = aligned_text

#         return cls(
#             contents, title, events, border_color, title_color, border_type, base_color
#         )


# x = Matrix.from_str(
#     """HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |                               |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|"""
# )
# x.color(Colors.RED, rect_range(Coord(5, 20), Coord(2, 5)))

# import tkinter as tk
# from tkinter import font


# class Text:
#     def update(self, key):
#         self.x[self.pos].value = " "

#         print(key.keysym)
#         if key.keysym == "a":
#             self.pos.x -= 1
#         elif key.keysym == "s":
#             self.pos.y += 1
#         elif key.keysym == "w":
#             self.pos.y -= 1
#         elif key.keysym == "d":
#             self.pos.x += 1

#         self.x[self.pos].value = "x"

#         self.text.configure(state="normal")

#         self.text.delete("1.0", "end")

#         last_coord = Coord(0, 0)
#         for coord in self.x.coords:
#             cell = self.x[coord]

#             if coord.y != last_coord.y:
#                 self.text.insert(f"{coord.y + 1}.{last_coord.x}", "\n")

#             self.text.insert(f"{coord.y + 1}.{coord.x}", cell.value)
#             self.text.tag_add("center", "1.0", "end")
#             if cell.color == Colors.RED:
#                 self.text.tag_add("red", f"{coord.y + 1}.{coord.x}")

#             last_coord = coord
#         # last_coord = Coord(5, 5)
#         # for coord in [coord for coord in self.x.coords]:
#         #     cell = self.x[coord]

#         #     if coord.y != last_coord.y:
#         #         self.text.insert(f"{coord.y + 6}.{last_coord.x + 5}", "\n")

#         #     self.text.insert(f"{coord.y + 6}.{coord.x + 5}", cell.value)
#         #     self.text.tag_add("center", "1.0", "end")
#         #     if cell.color == Colors.RED:
#         #         self.text.tag_add("red", f"{coord.y + 6}.{coord.x + 5}")

#         #     last_coord = coord

#         self.text.configure(state="disabled")

#     def __init__(self, x: Matrix):
#         self.x = x
#         self.pos = Coord(5, 10)

#         def disable_text_select(event):
#             text.tag_remove("sel", "1.0", "end")
#             return "break"

#         def center(event=None):
#             y, x_ = root.winfo_height(), root.winfo_width()
#             new_font_size = round(
#                 min(x_, y) / 25
#             )  # Adjust the scaling factor as per your preference

#             #font1 = font.Font(root, family="Consolas", size=new_font_size)
#             text.config(font=("Consolas", new_font_size))

#             s = Size(y, x_)
#             # 1.71 height to width (width to height 0.583)
#             size = x.size
#             size.y *= round(new_font_size * 1.65)
#             size.x *= round(new_font_size * 0.737)

#             s -= size
#             s = s.center

#             text.place(x=s.x, y=s.y)

#         text = tk.Text(
#             root,
#             font=("Consolas", 20),
#             background="#2A3439",
#             foreground="white",
#             # highlightbackground=root["background"],
#             # highlightcolor=root["background"],
#             # highlightthickness=0,
#             bd=0,  # remove border without changing size
#             # pady=300
#         )
#         text.bind("<Button-1>", disable_text_select)

#         center()

#         text.tag_config("red", foreground="red", justify="center")
#         text.tag_config("center")

#         last_coord = Coord(0, 0)
#         for coord in self.x.coords:
#             cell = self.x[coord]

#             if last_coord == Coord(0, 0):
#                 print(coord)
#             if coord.y != last_coord.y:
#                 text.insert(f"{coord.y + 1}.{last_coord.x}", "\n")

#             text.insert(f"{coord.y + 1}.{coord.x}", cell.value)
#             text.tag_add("center", "1.0", "end")
#             if cell.color == Colors.RED:
#                 text.tag_add("red", f"{coord.y + 1}.{coord.x}")

#             last_coord = coord

#         text.configure(state="disabled")

#         self.text = text

#         root.bind("<Configure>", center)
#         root.bind("<KeyPress>", self.update)


# root = tk.Tk()

# root.geometry("700x520")
# root.minsize(300, 250)
# root.title("Pybattle")
# root.configure(bg="#2A3439")

# Text(x)


# root.mainloop()


# import tkinter as tk
# from tkinter.font import Font


# def resize_font(event):
#     new_font_size = round(
#         int(min(event.width, event.height) / 20) * 0.75
#     )  # Adjust the scaling factor as per your preference
#     label.config(font=("Consolas", new_font_size))


# def key_press(event):
#     print("Key pressed:", event.keysym)


# root = tk.Tk()
# root.geometry("500x600")

# label = tk.Label(
#     root,
#     text="""
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |                               |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|
# """,
#     font=("Consolas", 10),
# )
# label.pack(fill=tk.BOTH, expand=True)


# root.bind("<Configure>", resize_font)
# root.bind("<KeyRelease>", key_press)

# root.minsize(250, 250)
# root.title("Pybattle")
# root.mainloop()

# root = tk.Tk()

# # 'Consolas, 'Courier New', monospace'

# font = Font(family='Consolas')

# label = tk.Label(root, text="""
# HOME____________________________
# |  _____  | []             |    |
# |  |   |  | []             |____|
# |  |   |__| []             |====|
# |__|                       |====|
# |      X                        |
# |                               |
#                       () ____   |
# |                        [==]   |
# |     __              [|      | |
# | [= |__| =]          [|  ()  | |
# |                     [|      | |
# |_______________________________|""", font=font).pack()


# root.mainloop()
