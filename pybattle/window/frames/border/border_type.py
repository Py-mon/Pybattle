from __future__ import annotations

from pybattle.types_ import Direction, JunctionDict, Thickness
from pybattle.window.grid.matrix import Cell
from pybattle.window.frames.border.junction_table import get_junction


class BorderType:
    def __init__(
        self,
        top_right: JunctionDict,
        top_left: JunctionDict,
        bottom_right: JunctionDict,
        bottom_left: JunctionDict,
        horizontal: JunctionDict,
        vertical: JunctionDict,
    ) -> None:
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left
        self.horizontal = horizontal
        self.vertical = vertical

    @property
    def top_right_cell(self):
        return Cell(self.top_right)

    @property
    def top_left_cell(self):
        return Cell(self.top_left)

    @property
    def bottom_right_cell(self):
        return Cell(self.bottom_right)

    @property
    def bottom_left_cell(self):
        return Cell(self.bottom_left)

    @property
    def horizontal_cell(self):
        return Cell(self.horizontal)

    @property
    def vertical_cell(self):
        return Cell(self.vertical)

    def __repr__(self) -> str:
        return (
            f"{self.top_right_cell}{self.horizontal_cell * 4}{self.top_left_cell}\n"
            f"{self.vertical_cell}    {self.vertical_cell}\n"
            f"{self.bottom_right_cell}{self.horizontal_cell * 4}{self.bottom_left_cell}\n"
        )


def _uniform(
    thickness: Thickness,
) -> tuple[
    JunctionDict, JunctionDict, JunctionDict, JunctionDict, JunctionDict, JunctionDict
]:
    return (
        {Direction.DOWN: thickness, Direction.RIGHT: thickness},
        {Direction.DOWN: thickness, Direction.LEFT: thickness},
        {Direction.UP: thickness, Direction.RIGHT: thickness},
        {Direction.UP: thickness, Direction.LEFT: thickness},
        {Direction.LEFT: thickness, Direction.RIGHT: thickness},
        {Direction.UP: thickness, Direction.DOWN: thickness},
    )


class Borders:
    """
    ```
    Thin:
        ╭───╮
        │   │
        ╰───╯
    Thick:
        ┏━━━┓
        ┃   ┃
        ┗━━━┛
    Double:
        ╔═══╗
        ║   ║
        ╚═══╝
    """

    THIN = BorderType(*_uniform(Thickness.THIN))
    THICK = BorderType(*_uniform(Thickness.THICK))
    DOUBLE = BorderType(*_uniform(Thickness.DOUBLE))
