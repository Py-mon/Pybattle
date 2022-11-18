WEIGHT_TO_SPEED = 1/3  # 30lb -> 10% Speed Decrease


class Armor:
    """A covering to protect and increase a `Humanoid's` defense in battle."""

    def __init__(
        self,
        defense_mult: float,
        weight: int,
        graphics: str = '',
    ) -> None:
        
        self.defense_mult = defense_mult
        self.graphics = graphics
        self.weight = weight
        self.speed_decrease_mult = self.weight * WEIGHT_TO_SPEED
        
    def __repr__(self) -> str:
        return self.function.__name__.capitalize()

class Weapon:
    """A tool used for increasing physical or magical damage for `Humanoids`."""

    def __init__(
        self,
        stat: str,
        mult: float,
        weight: int,
        graphics: str = '',
    ):
        self.stat = stat
        self.mult = mult
        self.weight = weight
        self.graphics = graphics
        self.speed_decrease_mult = self.weight * WEIGHT_TO_SPEED
        
    def __repr__(self) -> str:
        return self.function.__name__.capitalize()
