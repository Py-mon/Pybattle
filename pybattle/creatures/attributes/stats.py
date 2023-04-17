from numpy import random


def beta_value(min_: float = 0.05, max_: float = 0.1, curve: float = 5) -> float:
    """Generate a random value from a beta curve"""
    return min_ + (max_ - min_) * random.beta(curve, curve)


class Stat:
    """A value with:
    - Base - The starting value.
    - Level Point - The amount that the starting value increases on leveling up.
    - Special Point - A unchangeable value that gets added to the starting value.
    - Skill Point - Increases with more battle experience which increases the value.
    """

    def __init__(
        self,
        base: float = ...,
        level_point: float = ...,
        special_point: float = ...,
        skill_point: float = ...,
    ) -> None:
        if base is ...:
            base = beta_value(75, 100)
        if level_point is ...:
            level_point = beta_value()
        if special_point is ...:
            special_point = beta_value()
        if skill_point is ...:
            skill_point = beta_value()

        self.base = base
        self.level_point = level_point
        self.special_point = special_point
        self.skill_point = skill_point
        self.bonus = 0.0  # Used for traits, and other bonuses before battle.
        self.battle_bonus = 0.0  # Use in battle.

    def __repr__(self) -> str:
        return str(self.value) + ";" + str(self.battle_bonus)

    @property
    def value(self) -> float:
        """The total value calculating the points"""
        return round(
            self.base
            * (1 + self.special_point)
            * (1 + self.skill_point)
            * (1 + self.bonus)
        )


class Stats:
    """A dict of Stats for attack, magic, defense, health, energy, and speed"""

    STATS = ["attack", "magic", "defense", "health", "energy", "speed"]

    def __init__(
        self,
        bases: dict[str, int] = {},
        level_points: dict[str, int] = {},
        special_points: dict[str, int] = {},
        skill_points: dict[str, int] = {},
    ) -> None:
        self.stats = {
            stat: Stat(
                bases.get(stat, ...),
                level_points.get(stat, ...),
                special_points.get(stat, ...),
                skill_points.get(stat, ...),
            )
            for stat in self.STATS
        }

        self.bases = {key: value.base for key, value in self.stats.items()}
        self.total = sum(bases.values())
        self.level_points = {
            key: value.level_point for key, value in self.stats.items()
        }
        self.special_points = {
            key: value.special_point for key, value in self.stats.items()
        }
        self.skill_points = {
            key: value.skill_point for key, value in self.stats.items()
        }

    def __repr__(self) -> str:
        return f"Stats({self.stats})"

    def __getitem__(self, key: str) -> Stat:
        return self.stats[key]
