from typing import Optional

from creatures.grpahics.graphics import Body, HelmetGraphics, WeaponGraphics
from pybattle.screen.grid.matrix import Matrix

WEIGHT_TO_SPEED = 1 / 3  # 1lb -> 0.33% Speed Decrease


class Reinforcement:
    def __init__(
        self,
        name: str,
        stat: str,
        mult: float,
        weight: int = 0,
        graphics: Optional[Body | WeaponGraphics | HelmetGraphics] = None,
    ) -> None:
        self.name = name
        self.stat = stat
        self.mult = mult
        self.graphics = graphics
        self.weight = weight
        self.speed_decrease_mult = 1 + self.weight * WEIGHT_TO_SPEED / 100


class Armor(Reinforcement):
    """A covering to protect and increase a Humanoid's defense in battle."""

    def __init__(
        self,
        name: str,
        stat: str,
        mult: float,
        weight: int = 0,
        graphics: Optional[Body] = None,
    ) -> None:
        super().__init__(name, stat, mult, weight, graphics)
        self.graphics: Optional[Body]


class Helmet(Reinforcement):
    def __init__(
        self,
        name: str,
        stat: str,
        mult: float,
        weight: int = 0,
        graphics: Optional[HelmetGraphics] = None,
    ) -> None:
        super().__init__(name, stat, mult, weight, graphics)
        self.graphics: Optional[HelmetGraphics]


class Weapon(Reinforcement):
    """A tool used for increasing physical or magical damage for Humanoids."""

    def __init__(
        self,
        name: str,
        stat: str,
        mult: float,
        weight: int = 0,
        graphics: Optional[WeaponGraphics] = None,
    ) -> None:
        super().__init__(name, stat, mult, weight, graphics)
        self.graphics: Optional[WeaponGraphics]
