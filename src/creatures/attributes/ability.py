"""A talent or skill for a `Creature`."""

from __future__ import annotations

from typing import Callable

from src.types_ import Attacker, Creature, Defender, User


class Ability:
    """A talent or skill for a `Creature`."""

    def __init__(
        self,
        function: Callable[[User, list[Attacker], list[Defender]], None],
        condition: Callable[[], bool] = lambda: True,
        activations: int = 1,
    ) -> None:
        self.function = function
        self.condition = condition
        self.activations = activations

    def __repr__(self) -> str:
        return self.function.__name__.capitalize()

    def activate(
        self,
        user: User,
        attackers: list[Creature],
        defenders: list[Creature],
    ) -> bool | None:
        """Activate the ability if the conditions aren't right or it is out of activations.

        Returns `True` on success and `False` on failure."""
        if self.condition and self.activations > 0:
            self.activations -= 1
            self.function(user, attackers, defenders)
            return True
        else:
            return False
