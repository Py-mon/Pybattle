from typing import Any, Optional

from pybattle.creatures.attributes.ability import Ability
from pybattle.creatures.attributes.element import Element
from pybattle.creatures.attributes.item import Item
from pybattle.creatures.attributes.move import Move
from pybattle.creatures.attributes.reinforcements import Armor, Helmet, Weapon
from creatures.grpahics.graphics import (
    Body,
    Character,
    Face,
    Head,
    HelmetGraphics,
    MaleHair,
    WeaponGraphics,
)
from pybattle.creatures.pymon import Pymon
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.matrix import Matrix


class Humanoid(Pymon):
    """A human or human like creature that is the same as a Pymon but with armor and weapons. Cannot be bred."""

    def __init__(
        self,
        weapon: Optional[Weapon] = None,
        helmet: Optional[Helmet] = None,
        head: Optional[Head] = None,
        armor: Optional[Armor] = None,
        nickname: Optional[str] = None,
        bases: Optional[dict[str, float]] = None,
        level_points: dict[str, float] = {},
        special_points: dict[str, float] = {},
        skill_points: dict[str, float] = {},
        trait_amount: Optional[int] = None,
        element: Optional[Element] = None,
        abilities: Optional[tuple[Ability, ...]] = None,
        unique_abilities: Optional[tuple[Ability, ...]] = None,
        item: Optional[Item] = None,
        moves: Optional[list[Move]] = None,
        starting_level: Optional[int] = None,
    ):
        super().__init__(
            nickname,
            bases,
            level_points,
            special_points,
            skill_points,
            trait_amount,
            element,
            abilities,
            unique_abilities,
            item,
            moves,
            starting_level,
        )

        self.weapon = weapon
        if self.weapon is not None:
            self.bonuses[self.weapon.stat] = self.weapon.mult
            self.bonuses["speed"] = self.weapon.speed_decrease_mult
            weapon_graphics = self.weapon.graphics
        else:
            weapon_graphics = None

        body_ = Body(
            """\
  _─╵───╵─_            
 ╱ │     │ ╲            
 ╲ │_____│ ╱            
  ^│ ╭─╮ │^            
   │ │ │ │            
   │_│ │_│           """
        )

        self.armor = armor
        if self.armor is not None:
            self.bonuses["defense"] = self.armor.mult
            self.bonuses["speed"] = self.armor.speed_decrease_mult
            body = self.armor.graphics or body_
        else:
            body = body_

        self.helmet = helmet
        if self.helmet is not None:
            self.bonuses["defense"] = self.helmet.mult
            self.bonuses["speed"] = self.helmet.speed_decrease_mult
            head_ = self.helmet.graphics or head
        else:
            head_ = head

        self.graphics: Character = Character(body, head_, weapon_graphics)

    def breed(self, *_, **__) -> None:
        raise AttributeError("Breeding is not allowed for Humanoids.")


b = Body(
    """
  _─╵───╵─_          
 ╱ │     │ ╲          
 ╲ │_____│ ╱          
  ^│ ╭─╮ │^          
   │ │ │ │          
   │_│ │_│          
        """
)

h = Head(MaleHair(Cell.from_str("_-/|\\-_")[0]), Face(Cell(","), Cell("-")))
w = WeaponGraphics(
    Matrix(
        Cell.from_str(
            """
            
    
            
_ ^
 ╲│
  ^
  │
  │
  │"""
        )
    ),
    None,
)


human = Humanoid(
    bases={"attack": 40, "defense": 30},
    weapon=Weapon("", "attack", 1.2, graphics=w),
    head=h,
    armor=Armor("", "defense", 1.1, graphics=b),
)
print(human.graphics.left)
print(human.get_stat("attack"))
print(human.get_stat("defense"))
