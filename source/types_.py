from typing import TYPE_CHECKING, TypeAlias, Union

if TYPE_CHECKING:
    from creatures.attributes.ability import Ability as Ability_
    from creatures.attributes.element import Element
    from creatures.attributes.item import Item as Item_
    from creatures.attributes.move import Move as Move_
    from creatures.attributes.reinforcements import Armor as Armor_
    from creatures.attributes.reinforcements import Weapon as Weapon_
    from creatures.attributes.status_ailment import \
        StatusAilment as StatusAilment_
    from creatures.attributes.trait import Trait as Trait_
    from creatures.humanoid import Humanoid as Humanoid_
    from creatures.pymon import Pymon as Pymon_
    from window.coord import Coord
    from window.size import Size
    

Creature = Union["Pymon_", "Humanoid_"]
Attacker = Creature
Defender = Creature
User = Creature

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
