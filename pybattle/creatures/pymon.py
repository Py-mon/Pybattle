from copy import deepcopy
from fractions import Fraction
from math import floor
from pprint import pformat
from random import choice, choices, randint, random, uniform
from string import ascii_letters, digits
from typing import Any, Optional, Self

from pybattle.creatures.attributes.ability import Ability
from pybattle.creatures.attributes.element import Element
from pybattle.creatures.attributes.item import Item
from pybattle.creatures.attributes.move import Move
from pybattle.creatures.attributes.stats import Stats
from pybattle.creatures.attributes.status_ailment import StatusEffect
from pybattle.creatures.attributes.trait import Trait
from pybattle.creatures.rand import Curve, roll
from pybattle.log.log import logger
from pybattle.screen.colors import Color, Colors
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.matrix import Matrix
from pybattle.types_ import Creature


def get_mult_from_stage(stage: int, stage_increase: float):
    if stage < 0:
        return 1 / (-stage * stage_increase + 1)
    else:
        return (stage * stage_increase + 1) / 1


class Pymon:
    """A wild animal. (aka, a Pokémon)"""

    TRAIT_AMOUNT = 2

    STARTING_LEVELS = [1, 2, 3, 4]
    STARTING_LEVEL_WEIGHTS = [1, 3, 4, 1]

    STARTING_MAX_XP = 100

    MAX_XP_INCREASE = 0.5

    UNIQUE_ABILITY_CHANCE = 1 / 128

    INHERITANCE_CHANCE = 1 / 4

    BASE_LEVEL_MULT = 1.1

    UP_WEIGHT = 2  # How many stat points you get per unique point.
    SP_WEIGHT = 0.25  # How many stat points you get per skill point.

    LESSER_STAT_STAGE = 1 / 3
    GREATER_STAT_STAGE = 1 / 2

    MINIMUM_STAT_BOOST = 0.4  # 0.4x
    MAXIMUM_STAT_BOOST = 2.5  # 2.5x

    INHERIT_CURVE = Curve.even(0, 50, 7)

    name: str = Self.__name__
    leveling_moves: dict[int, Move] = {}
    bases: dict[str, float] = {}
    element: Optional[Element] = None
    abilities: tuple[Ability, ...] = ()
    unique_abilities: tuple[Ability, ...] = ()
    species_graphics: Optional[str] = None
    bonuses: dict[str, float] = {}
    graphics: Optional[Matrix] = None

    def __init__(
        self,
        nickname: Optional[str] = None,
        bases: Optional[dict[str, float]] = None,
        level_points: dict[str, float] = {},
        unique_points: dict[str, float] = {},
        skill_points: dict[str, float] = {},
        trait_amount: Optional[int] = None,
        element: Optional[Element] = None,
        abilities: Optional[tuple[Ability, ...]] = None,
        unique_abilities: Optional[tuple[Ability, ...]] = None,
        item: Optional[Item] = None,
        moves: Optional[list[Move]] = None,
        starting_level: Optional[int] = None,
        bonuses: dict[str, float] = {},
    ) -> None:
        self.id = id(self)
        self.name: str = nickname or type(self).name

        self.level_points = level_points
        self.unique_points = unique_points
        self.skill_points = skill_points

        self.bases = bases or self.bases

        self.traits = Trait.generate(trait_amount or self.TRAIT_AMOUNT)
        if self.traits is None:
            logger.warning(
                f"Not enough traits established for {self.name}. {self.name} will have no traits."
            )
        else:
            for trait in self.traits:
                trait.function(self)

        self.element = element or self.element

        self.status_effects: list[StatusEffect] = []

        if roll(self.UNIQUE_ABILITY_CHANCE):
            abilities = abilities or self.abilities
            if abilities:
                self.ability = choice(abilities)
        else:
            abilities = unique_abilities or self.abilities
            if abilities:
                self.ability: Ability | None = choice(
                    unique_abilities or self.unique_abilities
                )

        self.item: Item | None = item

        self.graphics = (
            Matrix(Cell.from_str(self.species_graphics))
            if self.species_graphics is not None
            else self.species_graphics
        )

        self.targets: list[Creature] = []
        self.damage_to = 0.0

        self.moves = moves or []

        self.move: Move

        self.experience = 0.0
        self.max_experience = self.STARTING_MAX_XP

        self.stat_bonuses = {}
        self.lesser_stat_stages = {}  # 3 turns
        self.greater_stat_stages = {}  # 2 turns

        self._level: int = 1
        self.levels_bonus = {}
        self.level = starting_level or self.random_level

        for level, move in self.leveling_moves.items():
            if self.level >= level:
                self.moves.append(move)

        self.bonuses = (
            bonuses or type(self).bonuses or {key: 1 for key in self.bases.keys()}
        )
        

        self.temp_bonuses = {}

        self.graphics = type(self).graphics

        self.debug()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level: int):
        self._level = level
        for stat, _ in self.levels_bonus.items():
            self.levels_bonus[stat] *= self.level_points[stat]

    @property
    def random_level(self):
        return choices(type(self).STARTING_LEVELS, type(self).STARTING_LEVEL_WEIGHTS)[0]

    def get_max_stat(self, stat: str):
        bases = self.bases[stat]
        level_points_mult = self.level_points.get(stat, 0) / 100 + 1
        level_mult = level_points_mult * (
            type(self).BASE_LEVEL_MULT ** (self.level - 1)
        )
        unique_points = self.unique_points.get(stat, 0) * type(self).UP_WEIGHT
        skill_points = self.skill_points.get(stat, 0) * type(self).SP_WEIGHT
        points = (bases * level_mult + unique_points + skill_points) * self.bonuses.get(
            stat, 1
        )

        return points

    def get_stat(self, stat: str):
        # LESSER_STAT_STAGE = 1 / 3   # +0.33x
        # GREATER_STAT_STAGE = 1 / 2  # +0.50x

        # MINIMUM_STAT_BOOST = 3 / 4  # -0.75x
        # MAXIMUM_STAT_BOOST = 3 / 2  # +1.5x # 3 greaters

        lesser_stage = self.lesser_stat_stages.get(stat, 0)
        lesser_mult = get_mult_from_stage(lesser_stage, type(self).LESSER_STAT_STAGE)

        greater_stage = self.greater_stat_stages.get(stat, 0)
        greater_mult = get_mult_from_stage(greater_stage, type(self).GREATER_STAT_STAGE)

        stage_mult = min(
            max(greater_mult + lesser_mult - 1, type(self).MINIMUM_STAT_BOOST),
            type(self).MAXIMUM_STAT_BOOST,
        )

        return self.get_max_stat(stat) * stage_mult * self.temp_bonuses.get(stat, 1)

    def debug(self) -> None:
        """Debug all the stats."""
        logger.debug(pformat(self.__dict__))

    def element_mult(self, defending_element: Element) -> float:
        """Get a element multiplier by attacking `defending_elements`"""
        return self.move.element * defending_element

    def get_percentage_bar(
        self,
        stat: str,
        bar_amount: int = 20,
        other_color=Colors.DEFAULT,
        high_color=Colors.GREEN,
        medium_color=Colors.YELLOW,
        low_color=Colors.RED,
    ) -> Matrix:
        """Get a percentage bar.
        `━━━━━━━━━━━━━───────`
        """
        bars = max(
            round(self.get_stat(stat) / (self.get_max_stat(stat) / bar_amount)),
            1,
        )

        percent = self.get_stat(stat) / self.get_max_stat(stat)

        color = ""
        if percent >= 2 / 3:
            color = high_color
        elif percent >= 1 / 3:
            color = medium_color
        else:  # percent <= 1 / 3:
            color = low_color

        return Matrix(
            (Cell("━", color) * bars + Cell("─", other_color) * (bar_amount - bars),)
        )

    def breed(self, with_: Self, level: Optional[int] = None) -> Self:
        """Create a offspring between `self` and `with_`. The species with be `self`'s species and some stats will be inherited from `with_`"""

        def inherit(
            primary: dict[str, float], secondary: dict[str, float]
        ) -> dict[str, float]:
            dct = {}
            for key in secondary.keys():
                roll_ = roll(1, 2, 4)

                if roll_ == 1:
                    dct[key] = Curve.from_mean(
                        secondary[key], type(self).INHERIT_CURVE
                    ).num
                elif roll_ == 2:
                    dct[key] = Curve.from_mean(
                        primary[key], type(self).INHERIT_CURVE
                    ).num
                elif roll_ == 4:
                    dct[key] = type(self).INHERIT_CURVE.num

            return dct

        return type(self)(
            level_points=inherit(self.level_points, with_.level_points),
            unique_points=inherit(self.unique_points, with_.unique_points),
            starting_level=level or self.random_level,
        )
