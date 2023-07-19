from pathlib import Path
from typing import Optional, Self

from pybattle.types_ import CardinalDirection
from pybattle.window.sound import Sound


class Weather: # ☁☂☀
    active: list[Self] = []

    def __init__(
        self,
        sound: Optional[Sound] = None,
        particles: Optional[list[str]] = None,
        heaviness: int = 5,
        frequency: float = 0.12,
    ):
        self.particles = particles
        self.sound = sound
        self.heaviness = heaviness
        self.frequency = frequency

        self.power = self.heaviness + 1 / self.frequency

        type(self).active.append(self)


class Rain(Weather): # rain icon: ⛆ ☁☂☀
    def __init__(
        self, wind: CardinalDirection, heaviness: int = 5, frequency: float = 0.12
    ):
        if wind == CardinalDirection.WEST:
            particles = ["/"]
        elif wind == CardinalDirection.EAST:
            particles = ["\\"]
        else:
            particles = ["|"]

        super().__init__(
            Sound("sounds/light_rain.mp3"), particles, heaviness, frequency
        )
        
        if self.power < 10:
            particles.append(".")
