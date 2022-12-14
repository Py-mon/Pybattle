from __future__ import annotations

from typing import Sequence

from pybattle.log import Logger
from pybattle.types_ import ElementReference


class Element:
    """Determines the strengths and weaknesses of different `Creatures`."""
    elements: dict[str, "Element"] = {}

    @staticmethod
    def convert_element_references(elements_references: Sequence[ElementReference]) -> list["Element"]:
        """Changes all the strs in `elements` to their value in `Element.elements`. 
        Removes the value if they are not in `Element.elements`. Returns it after the process."""
        elements: list["Element"] = []
        for element in elements_references:
            if isinstance(element, str):
                if element in Element.elements:
                    elements.append(Element.elements[element])
                else:
                    Logger.warning(
                        f'{element} is not an active element. It is not been added.')
            else:
                elements.append(element)
        return elements

    def __init__(
        self,
        name: str,
        strengths: list[ElementReference],
        resistances: list[ElementReference],
    ) -> None:
        self.name = name
        self.strengths = strengths
        self.resistances = resistances

        Element.elements[self.name] = self

    def __repr__(self) -> str:
        return self.name.capitalize()

    def attack_mult(self, element_references: Sequence[ElementReference]) -> float | int:
        """The multiplier of `self.element` attacking `elements_references`."""
        elements = self.convert_element_references(element_references)

        mult = 1.0
        for element in elements:
            if self.name in element.resistances:
                mult *= 1/2
            for strength in self.strengths:
                if isinstance(strength, str):
                    if element.name == strength:
                        mult *= 2
                elif isinstance(strength, Element):
                    if element.name == strength.name:
                        mult *= 2
        if mult == 1/4:
            return 0
        return mult
