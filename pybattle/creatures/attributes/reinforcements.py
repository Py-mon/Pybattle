from typing import Optional

from pybattle.creatures.graphics.graphics import Body, HelmetGraphics, WeaponGraphics
from dataclasses import dataclass

WEIGHT_TO_SPEED = 1 / 4  # 1lb -> 0.25% Speed Decrease


@dataclass
class _Reinforcement:
    """A tool that increases a certain stat, but with the disadvantage of losing a little speed."""

    name: str
    stat: str
    mult: float
    weight: int = 0
    graphics: Optional[Body | WeaponGraphics | HelmetGraphics] = None

    def __post_init__(self) -> None:
        self.speed_decrease_mult = 1 + self.weight * WEIGHT_TO_SPEED / 100


@dataclass
class Armor(_Reinforcement):
    """A covering to protect and increase a Humanoid's defense in battle."""

    graphics: Optional[Body] = None


@dataclass
class Helmet(_Reinforcement):
    """A covering to protect a Humanoid's head, increasing a their defense in battle."""

    graphics: Optional[HelmetGraphics]


@dataclass
class Weapon(_Reinforcement):
    """A tool used for increasing damage for Humanoids."""

    graphics: Optional[WeaponGraphics]
