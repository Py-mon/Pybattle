"""All the Types."""

from typing import TYPE_CHECKING, TypeAlias, Union

if TYPE_CHECKING:
    from src.creatures.attributes.ability import Ability as Ability_
    from src.creatures.attributes.element import Element
    from src.creatures.attributes.item import Item as Item_
    from src.creatures.attributes.move import Move as Move_
    from src.creatures.attributes.reinforcements import Armor as Armor_
    from src.creatures.attributes.reinforcements import Weapon as Weapon_
    from src.creatures.attributes.status_ailment import \
        StatusAilment as StatusAilment_
    from src.creatures.attributes.trait import Trait as Trait_
    from src.creatures.humanoid import Humanoid as Humanoid_
    from src.creatures.pymon import Pymon as Pymon_
    from src.window.color import Color as Color_
    from src.window.coord import Coord
    from src.window.screen import AnsiEscapeCode as AnsiEscapeCode_
    from src.window.size import Size


Creature = Union["Pymon_", "Humanoid_"]
Attacker = Creature
Defender = Creature
User = Creature

Color: TypeAlias = "Color_"
AnsiEscapeCode: TypeAlias = "AnsiEscapeCode_"
AnsiEscapeCodeOrColor = Union[Color, AnsiEscapeCode]  # TODO: Please rename

Armor: TypeAlias = "Armor_"
Weapon: TypeAlias = "Weapon_"
Ability: TypeAlias = "Ability_"
Item: TypeAlias = "Item_"
Move: TypeAlias = "Move_"
StatusAilment: TypeAlias = "StatusAilment_"
Trait: TypeAlias = "Trait_"
Humanoid: TypeAlias = "Humanoid_"

ElementReference: TypeAlias = Union[str, "Element"]

CoordReference: TypeAlias = Union["Coord", tuple]

SizeReference: TypeAlias = Union["Size", tuple]
