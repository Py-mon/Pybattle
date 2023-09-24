from typing import Callable, Optional

from pybattle.types_ import Attacker, Creature, Defender, User
from dataclasses import dataclass


@dataclass
class Ability:
    """A talent or skill for a Creature."""

    name: str
    function: Callable[[User, list[Attacker], list[Defender]], None]
    condition: Callable[[], bool] = lambda: True
    max_activations: int = 1
    desc: Optional[str] = None

    def __repr__(self) -> str:
        return f"{type(self).__name__}:{self.name}"

    def activate(
        self,
        user: User,
        attackers: list[Attacker],
        defenders: list[Defender],
    ) -> bool | None:
        """Activate the ability if the conditions aren't right or it is out of activations.

        Returns `True` on success and `False` on failure."""
        if not self.condition or self.max_activations <= 0:
            return False

        self.max_activations -= 1
        self.function(user, attackers, defenders)
        return True
