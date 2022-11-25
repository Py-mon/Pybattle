from source.window.coord import Coord, CoordList
from source.window.matrix import Matrix
from source.window.size import Size
from source.types_ import SizeReference, CoordReference
from .screen import Cursor


class Frame:
    def __init__(
        self,
        size: SizeReference
    ) -> None:
        self.size = Size.convert_reference(size)

        self.width = self.size.width
        self.height = self.size.height

        self._update_frame()

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, to: int):
        self._width = to
        self._update_frame()

    @property
    def height(self) -> int:
        return self._width

    @height.setter
    def height(self, to: int):
        self._height = to
        self._update_frame()

    @property
    def icols(self):
        return self.width - 1

    @property
    def irows(self):
        return self.height - 1

    def _update_frame(self) -> None:
        try:
            frame = f'╭{"─" * (self.width - 2)}╮\n'
            for _ in range(self.height - 2):
                frame += f'│{" " * (self.width - 2)}│\n'
            frame += f'╰{"─" * (self.width - 2)}╯\n'
        except Exception:
            raise ValueError(f'Invalid Frame')

        self.matrix = Matrix(frame)

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
        frame: "Frame",  # Only Frames can be added not Windows (so not Self)
        pos: CoordReference = Coord(0, 0),
    ) -> None:
        pos = Coord.convert_reference(pos)
        top_left = pos

        top_right = pos + frame.top_right_corner
        bottom_left = pos + frame.bottom_left_corner
        bottom_right = pos + frame.bottom_right_corner

        result = str(self.matrix)

        result += Cursor.move(pos).code

        if top_left in self.top_edge_positions:
            frame.matrix[*top_left.reverse] = '┬'
        elif top_left in self.left_edge_positions:
            frame.matrix[*top_left.reverse] = '├'

        if top_right in self.top_edge_positions:
            frame.matrix[*top_right.reverse] = '┬'
        elif top_right in self.right_edge_positions:
            frame.matrix[*top_right.reverse] = '┤'

        if bottom_left in self.top_edge_positions:
            frame.matrix[*bottom_left.reverse] = '┴'
        elif bottom_left in self.left_edge_positions:
            frame.matrix[*bottom_left.reverse] = '├'

        if bottom_right in self.top_edge_positions:
            frame.matrix[*bottom_right.reverse] = '┴'
        elif bottom_right in self.right_edge_positions:
            frame.matrix[*bottom_right.reverse] = '┤'

        result += str(frame.matrix)

        # TEST
        length = set()
        for line in result.splitlines(True):
            valid = True
            length.add(len(line))
            if len(length) > 1:
                print(line)
                valid = False

            print(valid)

        self.matrix = Matrix(result)


class Window(Frame):
    pass
