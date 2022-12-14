from copy import deepcopy
from fractions import Fraction
from math import floor
from random import choice, choices, randint
from string import ascii_letters, digits
from typing import Any, Dict, Self

from pybattle.creatures.attributes.ability import Ability
from pybattle.creatures.attributes.element import Element
from pybattle.creatures.attributes.item import Item
from pybattle.creatures.attributes.move import Move
from pybattle.creatures.attributes.stats import Stats
from pybattle.creatures.attributes.status_ailment import StatusAilment
from pybattle.creatures.attributes.trait import Trait
from pybattle.log import Logger
from pybattle.types_ import Creature, ElementReference, Humanoid
from pybattle.window.color import Colors


class ID:
    """A unique ID."""
    _ids = []

    def __new__(cls, length: int = 12) -> str:
        """Create a unique ID."""
        id_ = "".join(choices(ascii_letters + digits, k=length))
        while id_ in cls._ids:
            id_ = "".join(choices(ascii_letters + digits, k=length))
        cls._ids.append(id_)
        return id_


def roll(chance: Fraction) -> bool:
    """Returns False on common and True on rare.

    >>> roll(Fraction(1/4))  # 1/4 chance to return True, 3/4 chance to return False."""
    return choices([True, False], [chance, Fraction(chance.denominator - chance.numerator, chance.denominator)])[0]


class Pymon:
    """A wild animal. (AKA: A Pokémon)"""
    TRAIT_AMOUNT = 2

    STARTING_LEVEL = 1
    STARTING_MAX_XP = 100

    MAX_XP_INCREASE = .5

    UNIQUE_ABILITY_CHANCE = Fraction(1, 128)

    INHERITANCE_CHANCE = Fraction(1, 4)

    def __init_subclass__(cls) -> None:
        """Set default attrs."""
        if 'name' not in cls.__dict__:
            cls.name = cls.__name__

        if 'leveling_moves' not in cls.__dict__:
            cls.leveling_moves: dict[int, Move] = {}

        if 'bases' not in cls.__dict__:
            cls.bases: dict[str, int] = {}

        if 'elements' not in cls.__dict__:
            cls.elements: list[ElementReference] = []

        if 'abilities' not in cls.__dict__:
            cls.abilities: list[Ability] = []

        if 'unique_abilities' not in cls.__dict__:
            cls.unique_abilities: list[Ability] = []

        if 'graphics' not in cls.__dict__:
            cls.graphics: str = ''

    def __init__(self, dct: dict[str, Any] = {}) -> None:
        """
        Args:
            - `'nickname': str`
            - `'bases': dict[str, int]`
            - `'level_points': dict[str, int]`
            - `'special_points': dict[str, int]`
            - `'skill_points': dict[str, int]`
            - `'trait_amount': int`
            - `'elements': list[ElementReference]`
            - `'abilities': list[Ability]`
            - `'unique_abilities': list[Ability]`
            - `'item': Item`
            - `'graphics': str`
            - `'moves': list[Move]`
            - `'starting_level': int`
            """
        self.__init_subclass__()

        Logger.info(
            f'---------------------- {self.name} Created ----------------------')

        self.id_ = ID()
        self.name: str = dct.get('nickname', self.name)

        self.stats = Stats(
            dct.get('bases', self.bases),
            dct.get('level_points', {}),
            dct.get('special_points', {}),
            dct.get('skill_points', {})
        )
        self.max_stats = deepcopy(self.stats)

        self.traits = Trait.generate(
            dct.get('trait_amount', self.TRAIT_AMOUNT))
        if self.traits is None:
            Logger.warning(
                f'Not enough traits established for {self.name}. {self.name} will have traits.')
        else:
            for trait in self.traits:
                trait.function(self)

        self.elements = Element.convert_element_references(
            dct.get('elements', self.elements))

        self.status_ailments: list[StatusAilment] = []

        if roll(self.UNIQUE_ABILITY_CHANCE):
            abilities = dct.get('abilities', self.abilities)
            if abilities:
                self.ability: Ability | None = choice(abilities)
        else:
            abilities = dct.get('unique_abilities', self.abilities)
            if abilities:
                self.ability: Ability | None = choice(
                    dct.get('unique_abilities', self.unique_abilities))

        self.item: Item | None = dct.get('item')

        self.graphics: str = dct.get('graphics', self.graphics)

        self.targets: list[Creature] = []
        self.damage_to = 0.0

        self.moves: list[Move] = dct.get('moves', [])
        self.move: Move

        self.experience = 0.0
        self.max_experience = self.STARTING_MAX_XP
        self.level: int = 1
        self.level_to(dct.get('starting_level', self.STARTING_LEVEL))

        self.debug()

    def debug(self) -> None:
        """Debug all the stats."""
        Logger.debug(str(self.__dict__))

    def element_mult(self, defending_elements: list[ElementReference]) -> float | int:
        """Get a element multiplier by attacking `defending_elements`."""
        return self.move.element.attack_mult(defending_elements)

    def get_percentage_bar(
        self,
        stat: str,
        bar_amount: int = 20,
        high_color=Colors.GREEN,
        medium_color=Colors.YELLOW,
        low_color=Colors.RED,
    ) -> str:
        """Get a percentage bar.

        `||||||||||||||||....`

        `░░░░░░░░░░░░░░░░....`

        `▒▒▒▒▒▒▒▒............`

        `▓▓..................`

        `━━━━━━━━━━━━━───────`
        """
        bars = round(self.stats[stat].value /
                     (self.max_stats[stat].value / bar_amount))

        if floor(bars) == 0:
            bars = 1

        percent = self.stats[stat].value / self.max_stats[stat].value

        color = ''
        if percent >= 2/3:
            color = high_color
        elif percent >= 1/3:
            color = medium_color
        elif percent <= 1/3:
            color = low_color

        bars = f"{str(color) + '━' * bars + str(Colors.DEFAULT):─<{bar_amount + len(str(color)) + len(str(Colors.DEFAULT))}}"
        return bars

    def level_up(self) -> None:
        """Level up once."""
        stats = choices(list(self.stats.stats.keys()), k=randint(2, 3))
        for stat in stats:
            self.stats[stat].bonus *= 1 + self.stats[stat].level_point
        self.level += 1
        self.max_experience *= 1 + self.MAX_XP_INCREASE

        for level, move in self.leveling_moves.items():
            if level >= self.level:
                self.moves.append(move)

    def level_to(self, level: int) -> None:
        """Level up to a certain `level`. 

        Does nothing if `level` is below or equal to the current level. 
        """
        while self.level < level:
            self.level_up()

    def breed(self, with_: Self, level: int = ...) -> Self:
        """Create a offspring between `self` and `with_`. The species with be `self`'s species and some stats will be inherited from `with_`."""
        if isinstance(with_, Humanoid):
            raise AttributeError('Breeding is not allowed for Humanoids.')

        def inherit(common: Dict[str, float], rare: Dict[str, float]) -> Dict[str, float]:
            x = {}
            for key in common.keys():
                if roll(self.INHERITANCE_CHANCE):
                    x[key] = rare[key]
                else:
                    x[key] = common[key]
            return x
        
        if level is ...:
            level = randint(1, 5)

        return self.__class__({
            'level_points': inherit(self.stats.level_points, with_.stats.level_points),
            'special_points': inherit(self.stats.special_points, with_.stats.special_points),
            'skill_points': inherit(self.stats.skill_points, with_.stats.skill_points),
            'starting_level': level
        })
