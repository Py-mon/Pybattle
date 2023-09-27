from copy import copy
from typing import Self
from dataclasses import dataclass


@dataclass
class Element:
    name: str
    mults: dict[str, float]

    @property
    def strengths(self):
        """All of the elements that are super effective (2x)."""
        return {element: mult for element, mult in self.mults.items() if mult == 2}

    @property
    def super_strengths(self):
        """All of the elements that are super duper effective (4x)."""
        return {element: mult for element, mult in self.mults.items() if mult == 4}

    @property
    def weaknesses(self):
        """All of the elements that are super duper effective (1/2x)."""
        return {element: mult for element, mult in self.mults.items() if mult < 0.5}
    
    @property
    def super_weaknesses(self):
        """All of the elements that are super duper effective (1/4x)."""
        return {element: mult for element, mult in self.mults.items() if mult < 0.5}

    @property
    def immunities(self):
        return {element: mult for element, mult in self.mults.items() if mult == 0}

    @property
    def neutrals(self):
        return {element: mult for element, mult in self.mults.items() if mult == 1}

    def __mul__(self, other: Self) -> float:
        """get the mult for self attacking other"""
        if "+" in other.name:
            mult = 1
            for element in other.name.split("+"):
                #mult *= self.mults.get(element, 1)
                mult = 1/(1/self.mults.get(element, 1)+1)
            return mult
        return self.mults.get(other.name, 1)

    def __add__(self, other: Self):
        """add two or more types together"""
        dct = copy(self.mults)
        for element, mult in other.mults.items():
            if element in dct:
                dct[element] *= mult
            else:
                dct[element] = mult
        return type(self)(f"{self.name}+{other.name}", dct)


fire = Element("fire", {"fire": 0.5, "water": 0.5})

# water = Element("water", {"water": 0.5, "fire": 2})

# print((fire) * (fire + water))


