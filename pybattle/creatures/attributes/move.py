from typing import Callable, Optional, Literal

from pybattle.creatures.attributes.element import Element
from pybattle.types_ import Attacker, Creature, Defender, Alignment, Level, Side
from pybattle.screen.frames.frame import Frame, Title
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.matrix import Grid
from pybattle.screen.grid.point import Size, Coord
from dataclasses import dataclass
from copy import copy


@dataclass
class Move:
    """A technique that a creature uses in battle."""

    name: str
    element: Element
    function: Callable[[list[Attacker], list[Defender]], None | Literal["start"]]
    tick: Optional[
        Callable[[list[Attacker], list[Defender]], None | Literal["end"]]
    ] = None
    energy_cost: int = 0
    strength: Optional[int] = None
    accuracy: int = 100
    type_: Optional[str] = None
    desc: Optional[str] = None

    def __post_init__(self):
        def add_titles(frame):
            frame.add_title(Title(self.name))
            frame.add_title(Title(self.element.name.capitalize(), Alignment.RIGHT))

        def add_text(frame, text: Grid, level: Level, side: Side):
            if side == Side.LEFT:
                frame.overlay(
                    text,
                    Coord(level.value + 2, 2),
                )
            else:
                frame.overlay_to_left(
                    text,
                    Coord(level.value + 2, -3),
                )

        strength = Grid(Cell.from_str(str(self.strength) + " STR"))
        energy_cost = Grid(Cell.from_str(str(self.energy_cost) + " EC"))
        accuracy = Grid(Cell.from_str(str(self.accuracy) + "% ACC"))
        type_ = Grid(Cell.from_str(str(self.type_)))

        self.frame = Frame(
            Cell.from_size(Size(1, 19)),
        )
        add_titles(self.frame)

        extended_frame = Frame(
            Cell.from_size(Size(2, 19)),
        )
        add_titles(extended_frame)

        if self.strength is None:
            add_text(self.frame, type_, Level.BOTTOM, Side.LEFT)
            add_text(self.frame, energy_cost, Level.BOTTOM, Side.RIGHT)

            self.top_extended_frame = copy(extended_frame)

            add_text(self.top_extended_frame, type_, Level.TOP, Side.LEFT)
            add_text(self.top_extended_frame, energy_cost, Level.TOP, Side.RIGHT)
            add_text(self.top_extended_frame, accuracy, Level.BOTTOM, Side.RIGHT)

            self.bottom_extended_frame = extended_frame  # dont have to copy

            add_text(self.bottom_extended_frame, type_, Level.BOTTOM, Side.LEFT)
            add_text(self.bottom_extended_frame, energy_cost, Level.BOTTOM, Side.RIGHT)
            add_text(self.bottom_extended_frame, accuracy, Level.TOP, Side.RIGHT)

        else:
            add_text(self.frame, strength, Level.BOTTOM, Side.LEFT)
            add_text(self.frame, energy_cost, Level.BOTTOM, Side.RIGHT)

            self.top_extended_frame = copy(extended_frame)

            add_text(self.top_extended_frame, strength, Level.TOP, Side.LEFT)
            add_text(self.top_extended_frame, energy_cost, Level.TOP, Side.RIGHT)
            add_text(self.top_extended_frame, type_, Level.BOTTOM, Side.LEFT)
            add_text(self.top_extended_frame, accuracy, Level.BOTTOM, Side.RIGHT)

            self.bottom_extended_frame = extended_frame  # dont have to copy

            add_text(self.bottom_extended_frame, strength, Level.BOTTOM, Side.LEFT)
            add_text(self.bottom_extended_frame, energy_cost, Level.BOTTOM, Side.RIGHT)
            add_text(self.bottom_extended_frame, type_, Level.TOP, Side.LEFT)
            add_text(self.bottom_extended_frame, accuracy, Level.TOP, Side.RIGHT)


