from typing import TYPE_CHECKING, TypeAlias, Union

if TYPE_CHECKING:
    from creatures.attributes.ability import Ability as Ability_
    from creatures.attributes.element import Element as Element_
    from creatures.attributes.item import Item as Item_
    from creatures.attributes.move import Move as Move_
    from creatures.attributes.reinforcements import Armor as Armor_, Weapon as Weapon_
    from creatures.attributes.status_ailment import StatusAilment as StatusAilment_
    from creatures.attributes.trait import Trait as Trait_
    from creatures.humanoid import Humanoid as Humanoid_
    from creatures.pymon import Pymon as Pymon_

Creature: TypeAlias = Union["Pymon_", "Humanoid_"]
Attacker: TypeAlias = Creature
Defender: TypeAlias = Creature
User: TypeAlias = Creature

Armor: TypeAlias = "Armor_"
Weapon: TypeAlias = "Weapon_"
Ability: TypeAlias = "Ability_"
Item: TypeAlias = "Item_"
Move: TypeAlias = "Move_"
StatusAilment: TypeAlias = "StatusAilment_"
Trait: TypeAlias = "Trait_"
Humanoid: TypeAlias = "Humanoid_"

ElementReference: TypeAlias = Union[str, "Element_"]
