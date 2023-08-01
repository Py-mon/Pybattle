from time import sleep
from typing import Callable, Optional, Self

from pybattle.log.errors import Error
from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.border.border_type import Borders, BorderType, Direction
from pybattle.screen.frames.frame import Frame
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.matrix import Matrix
from pybattle.screen.grid.point import Coord, Size
from pybattle.screen.window import keys_pressing
from pybattle.types_ import Alignment


def get_directions(from_: Coord, to: Coord) -> list[Direction]:
    directions = list()

    y1, x1 = from_
    y2, x2 = to

    if y1 < y2:
        directions.append(Direction.DOWN)
    if y1 > y2:
        directions.append(Direction.UP)

    if x1 < x2:
        directions.append(Direction.RIGHT)
    if x1 > x2:
        directions.append(Direction.LEFT)

    return directions


class VoidSelection:
    """The base selection"""

    def __init__(
        self,
        label: str,
        color: Color = Colors.DEFAULT,
    ) -> None:
        self.label = label
        self.color = color

        self.pos = Coord(0, 0)

    @property
    def size(self):
        s = Size.from_str(self.label).i
        s = Size(s.y + 1, s.x)
        return s


class Selection(VoidSelection):
    """A selection with a designated pos"""

    def __init__(
        self,
        label: str,
        pos: Coord,
        color: Color = Colors.DEFAULT,
    ) -> None:
        super().__init__(label, color)

        self.pos = pos


class FrameSelection(Selection):
    """A selection that has a frame around it"""

    def __init__(
        self,
        frame: Frame,
        pos: Coord,
    ) -> None:
        super().__init__("", pos)

        self.frame = frame

    @property
    def size(self):
        return self.frame.size


class SwitchSelection:
    def __init__(
        self,
        off: VoidSelection | Selection | FrameSelection,
        selected: VoidSelection | Selection | FrameSelection,
    ) -> None:
        if off.pos != selected.pos:
            raise Error("Cannot move a SwitchSelection's pos")
        elif off.label != selected.label and off.label != "" and selected.label != "":
            raise Error("Cannot change a SwitchSelection's label")

        self.off = off
        self.selected = selected

        self.directions: dict[Self, list[Direction]] = {}

    @property
    def label(self):
        return self.off.label

    @label.setter
    def label(self, label: str):
        self.off.label = label
        self.selected.label = label

    @property
    def pos(self):
        return self.off.pos

    @pos.setter
    def pos(self, pos: Coord):
        self.off.pos = pos
        self.selected.pos = pos


class Menu(Frame):
    def __init__(
        self,
        cells: list[list[Cell]],
        selections: list[SwitchSelection],
        title: Optional[str] = None,
        border_type: BorderType = Borders.THIN,
    ) -> None:
        super().__init__(cells, title, border_type)

        self.selections = selections

        # Set the starting selection to the one closest to the origin
        self.selection = selections[0]  # ? but not ordered?

        for current_selection in self.selections.copy():
            # Sort the selections by the closest ones first (when you press '►' it will go to the closest one to the right)

            self.selections.sort(key=lambda x: current_selection.pos.distance(x.pos))
            for selection in self.selections:
                # Exclude its own selection
                if selection != current_selection:
                    # Add the directions at the selected point to the other selection
                    current_selection.directions[selection] = get_directions(
                        current_selection.pos, selection.pos
                    )

        self.update()

    def update(self):
        for switch_selection in self.selections:
            if switch_selection == self.selection:
                selection = switch_selection.selected
            else:
                selection = switch_selection.off

            if isinstance(selection, FrameSelection):
                selection.frame.color_border(selection.frame.border_color)
                selection.frame.color_inside(selection.frame.base_color)
                self.add_frame(selection.frame, selection.pos)

            elif isinstance(selection, VoidSelection):
                self[selection.pos : selection.pos + selection.size] = Matrix(
                    Cell.from_str(selection.label)
                )

                self.color(
                    selection.color,
                    (selection.size + selection.pos).rect_range(selection.pos),
                )

    def switch(self):
        def move(direction: Direction) -> None:
            for selection, directions in self.selection.directions.items():
                if direction in directions:
                    self.selection = selection
                    break
        
        for key in keys_pressing:
            print(key)
            if key == 'a':
                move(Direction.LEFT)
            elif key == 's':
                move(Direction.DOWN)
            elif key == 'd':
                move(Direction.RIGHT)
            elif key == 'w':
                move(Direction.UP)
                
        self.update()
        self.recache()
        # print(self[Coord(4, 2)].color.name)
        # print(self.selection.label)


# def __init__(
#     self,
#     frame: Frame,
#     selections: list[SwitchSelection],
# ) -> None:
#     self.frame = frame

#     self.selections = selections

#     # Set the starting selection to the one closest to the origin
#     self.selection = selections[0]

#     for current_selection in self.selections.copy():
#         # Sort the selections by the closest ones first (when you press '►' it will go to the closest one to the right)
#         self.selections.sort(key=lambda x: current_selection.pos.distance(x.pos))
#         for selection in self.selections:
#             # Exclude its own selection
#             if selection != current_selection:
#                 # Add the directions at the selected point to the other selection
#                 current_selection.directions[selection] = get_directions(
#                     current_selection.pos, selection.pos
#                 )

#     self.update()

#     s = Scene(lambda: self.frame, Coord(5, 5))

#     def event():
#         self.update()

#         for key in Keyboard.pressed_keys:
#             if key == Key.right:
#                 self.right()
#             elif key == Key.left:
#                 self.left()
#             elif key == Key.up:
#                 self.up()
#             elif key == Key.down:
#                 self.down()
#             elif key == Key.enter:
#                 return self.selection.label

#         s.draw()

#     self.event = event

# def update(self):
#     frames = []
#     for switch_selection in self.selections:
#         if switch_selection == self.selection:
#             selection = switch_selection.selected
#         else:
#             selection = switch_selection.off

#         if isinstance(selection, FrameSelection):
#             frames.append((selection.frame, selection.pos))

#             selection.frame.update(
#                 selection.frame.border_color,
#                 base_color=selection.frame.base_color,
#             )

#         elif isinstance(selection, VoidSelection):
#             self.frame.contents[
#                 selection.pos : selection.pos + selection.size
#             ] = Matrix.from_str(selection.label)

#             self.frame.contents.color(
#                 selection.color,
#                 rect_range(selection.pos + selection.size, Coord(0, 0)),
#             )

#     self.frame.update(frames=frames + self.frame.frames)

# def move(self, direction: Direction) -> None:
#     for selection, directions in self.selection.directions.items():
#         if direction in directions:
#             self.selection = selection
#             break

# def right(self) -> None:
#     self.move(Direction.RIGHT)

# def left(self) -> None:
#     self.move(Direction.LEFT)

# def up(self) -> None:
#     self.move(Direction.UP)

# def down(self) -> None:
#     self.move(Direction.DOWN)

# @classmethod
# def centered_list(
#     cls,
#     frame: Frame,
#     selections: list[SwitchSelection],
#     align: Alignment = Alignment.MIDDLE,
# ) -> Self:
#     labels = [selection.off.label for selection in selections]
#     max_ = max(len(label) for label in labels)
#     size = Size.from_str("\n".join(labels))
#     size.x = max_

#     for i, selection in enumerate(selections):
#         print(repr(selection.label))
#         selection.label = align.align(selection.label, max_)
#         print(repr(selection.label))
#         slice_ = center_range(frame.size.inner, size)
#         selection.pos = Coord(slice_.start.y + i, slice_.start.x)

#     menu = cls(frame, selections)

#     # Link the first and the last item together
#     selections[-1].directions[selections[0]].append(Direction.UP)
#     selections[0].directions[selections[-1]].append(Direction.DOWN)

#     return menu


# class Menu:
#     def __init__(
#         self,
#         frame: Frame,
#         selections: list[SwitchSelection],
#     ) -> None:
#         self.frame = frame

#         self.selections = selections

#         # Set the starting selection to the one closest to the origin
#         self.selection = selections[0]

#         for current_selection in self.selections.copy():
#             # Sort the selections by the closest ones first (when you press '►' it will go to the closest one to the right)
#             self.selections.sort(key=lambda x: current_selection.pos.distance(x.pos))
#             for selection in self.selections:
#                 # Exclude its own selection
#                 if selection != current_selection:
#                     # Add the directions at the selected point to the other selection
#                     current_selection.directions[selection] = get_directions(
#                         current_selection.pos, selection.pos
#                     )

#         self.update()

#         s = Scene(lambda: self.frame, Coord(5, 5))

#         def event():
#             self.update()

#             for key in Keyboard.pressed_keys:
#                 if key == Key.right:
#                     self.right()
#                 elif key == Key.left:
#                     self.left()
#                 elif key == Key.up:
#                     self.up()
#                 elif key == Key.down:
#                     self.down()
#                 elif key == Key.enter:
#                     return self.selection.label

#             s.draw()

#         self.event = event

#     def update(self):
#         frames = []
#         for switch_selection in self.selections:
#             if switch_selection == self.selection:
#                 selection = switch_selection.selected
#             else:
#                 selection = switch_selection.off

#             if isinstance(selection, FrameSelection):
#                 frames.append((selection.frame, selection.pos))

#                 selection.frame.update(
#                     selection.frame.border_color,
#                     base_color=selection.frame.base_color,
#                 )

#             elif isinstance(selection, VoidSelection):
#                 self.frame.contents[
#                     selection.pos : selection.pos + selection.size
#                 ] = Matrix.from_str(selection.label)

#                 self.frame.contents.color(
#                     selection.color,
#                     rect_range(selection.pos + selection.size, Coord(0, 0)),
#                 )

#         self.frame.update(frames=frames + self.frame.frames)

#     def move(self, direction: Direction) -> None:
#         for selection, directions in self.selection.directions.items():
#             if direction in directions:
#                 self.selection = selection
#                 break

#     def right(self) -> None:
#         self.move(Direction.RIGHT)

#     def left(self) -> None:
#         self.move(Direction.LEFT)

#     def up(self) -> None:
#         self.move(Direction.UP)

#     def down(self) -> None:
#         self.move(Direction.DOWN)

#     @classmethod
#     def centered_list(
#         cls,
#         frame: Frame,
#         selections: list[SwitchSelection],
#         align: Alignment = Alignment.MIDDLE,
#     ) -> Self:
#         labels = [selection.off.label for selection in selections]
#         max_ = max(len(label) for label in labels)
#         size = Size.from_str("\n".join(labels))
#         size.x = max_

#         for i, selection in enumerate(selections):
#             print(repr(selection.label))
#             selection.label = align.align(selection.label, max_)
#             print(repr(selection.label))
#             slice_ = center_range(frame.size.inner, size)
#             selection.pos = Coord(slice_.start.y + i, slice_.start.x)

#         menu = cls(frame, selections)

#         # Link the first and the last item together
#         selections[-1].directions[selections[0]].append(Direction.UP)
#         selections[0].directions[selections[-1]].append(Direction.DOWN)

#         return menu


# print(
#     Menu(
#         Frame.box(Size(10, 25)),
#         [
#             SwitchSelection(
#                 Selection("Play", Coord(2, 2)),
#                 Selection("Play", Coord(2, 2), Colors.RED),
#             ),
#             SwitchSelection(
#                 Selection("Settings", Coord(4, 4)),
#                 Selection("Settings", Coord(4, 4), Colors.BLUE),
#             ),
#             SwitchSelection(
#                 Selection("Quit", Coord(6, 6)),
#                 Selection("Quit", Coord(6, 6), Colors.RED),
#             ),
#         ],
#     ).frame
# )

# Event(
#     Menu(
#         Frame.box(Size(10, 25)),
#         [
#             SwitchSelection(
#                 Selection("Play", Coord(2, 2)),
#                 Selection("Play", Coord(2, 2), Colors.RED),
#             ),
#             SwitchSelection(
#                 Selection("Settings", Coord(4, 4)),
#                 Selection("Settings", Coord(4, 4), Colors.BLUE),
#             ),
#             SwitchSelection(
#                 Selection("Quit", Coord(6, 6)),
#                 Selection("Quit", Coord(6, 6), Colors.RED),
#             ),
#         ],
#     ).event,
#     0.1,
# )

# e = Event(
#     Menu.centered_list(
#         Frame.box(Size(10, 25)),
#         [
#             SwitchSelection(
#                 VoidSelection("Play"),
#                 VoidSelection("Play", Colors.RED),
#             ),
#             SwitchSelection(
#                 VoidSelection("Settings"),
#                 VoidSelection("Settings", Colors.BLUE),
#             ),
#             SwitchSelection(
#                 VoidSelection("Quit"),
#                 VoidSelection("Quit", Colors.RED),
#             ),
#         ],
#     ).event,
#     0.1,
# )

# with key_listener:
#     EventGroup([e]).play()
