from typing import Callable, Optional, Literal

from pybattle.creatures.attributes.element import Element
from pybattle.types_ import Attacker, Creature, Defender
from pybattle.screen.frames.frame import Frame
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.matrix import Matrix
from pybattle.screen.grid.point import Size, Coord


class Move:
    """A technique that a creature uses in battle."""

    def __init__(
        self,
        name: str,
        element: Element,
        function: Callable[[list[Attacker], list[Defender]], None | Literal["start"]],
        tick: Optional[
            Callable[[list[Attacker], list[Defender]], None | Literal["end"]]
        ] = None,
        energy_cost: int = 0,
        strength: Optional[int] = None,
        accuracy: int = 100,
        type_: Optional[str] = None,
        desc: Optional[str] = None,
    ) -> None:
        self.name = name
        self.element = element
        self.accuracy = accuracy
        self.strength = strength
        self.type_ = type_
        self.tick = tick
        self.energy_cost = energy_cost
        self.function = function
        self.desc = desc

    def simple_frame(self):
        frame = Frame(
            Cell.from_size(Size(1, 16)),
            self.name.capitalize(),
            self.element.name.capitalize(),
        )
        frame.overlay(Matrix(Cell.from_str(str(self.strength) + " STR")), Coord(1, 2))
        frame.overlay(
            Matrix(Cell.from_str(str(self.energy_cost) + " EC")),
            Coord(1 , -(len(str(self.energy_cost))) - 5),
        )
        return frame
        ...


# ╭─ Wind Bash ─ Air ─╮
# │ 50 STR      25 EC │
# ╰───────────────────╯


print(Move('Wind Bash', Element('Air', {}), None, energy_cost=25, strength=50).simple_frame())




# def use(
#     self, attackers: list[Creature], defenders: list[Creature], width: int = 70
# ) -> None:
#     """Uses a move. Automatically resets damage, does element multipliers, and does damage."""
#     for attacker in attackers:
#         attacker.damage_to = 0
#     for defender in defenders:
#         defender.damage_to = 0
