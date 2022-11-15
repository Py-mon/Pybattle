from typing import Callable

from .element import Element
from types_ import Attacker, Creature, Defender, ElementReference

    
class Move:
    """A technique that a creature uses in battle."""

    def __init__(
        self,
        element: ElementReference,
        function: Callable[[list[Attacker], list[Defender]], None]
    ) -> None:
        self.element = Element.convert_element_references([element])[0]
        self.function = function
        
    def __repr__(self) -> str:
        return self.function.__name__.capitalize()

    def use(self, attackers: list[Creature], defenders: list[Creature], width: int = 70) -> None:
        """Uses a move. Automatically resets damage, does element multipliers, and does damage."""
        for attacker in attackers:
            attacker.damage_to = 0
        for defender in defenders:
            defender.damage_to = 0

        text_box = TextBox(height=3, width=width)

        for attacker in attackers:
            self.function(attackers, defenders)
            for target in attacker.targets:
                mult = attacker.move.element.attack_mult(target.elements)
                if mult == 2:
                    text_box.text = "It's super effective..!"
                elif mult == 0.5:
                    text_box.text = "It's not very effective..."
                elif mult == 4:
                    text_box.text = "It's super duper effective..!"
                elif mult == 0:
                    text_box.text = f"It's doesn't affect {target.name}..."
                target.damage_to *= mult
                target.stats['health'] -= target.damage_to
            attacker.stats['health'] -= attacker.damage_to

        print(text_box.speech())
