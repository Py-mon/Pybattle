from random import betavariate, choices, random
from typing import Self


def chance(chance: float) -> bool:
    """Return if random() <= chance"""
    return random() <= chance


def roll(*chances: float):
    return choices(chances, chances)[0]


class Curve:
    def __init__(self, low: float, high: float, a: float, b: float) -> None:
        self.low = low
        self.high = high
        self.a = a
        self.b = b

    @classmethod
    def even(cls, low: float, high: float, curve: float) -> Self:
        return cls(low, high, curve, curve)

    @classmethod
    def left(cls, low: float, high: float, curve: float) -> Self:
        return cls(low, high, 1, curve)

    @classmethod
    def right(cls, low: float, high: float, curve: float) -> Self:
        return cls(low, high, curve, 1)

    @classmethod
    def from_mean(cls, mean: float, curve: Self) -> Self:
        curve.high = (mean + curve.high) / 2
        curve.low = (mean + curve.low) / 2

        return curve

    @property
    def num(self):
        return self.low + (self.high - self.low) * betavariate(self.a, self.b)

    @property
    def mean(self):
        return ((self.a - 1) / (self.a + self.b - 2)) * (
            self.high - self.low
        ) + self.low


def get_curved_num(low: float, high: float, a: float = 5, b: float = 5) -> float:
    """Get a random number that is between low and high.

    if `a=1` and `b=1` then it is the same as `random()`.

    if `a>1 and b>1`, it becomes closer to the average of `low` and `high`.

    if `a<1 and b<1`, it becomes closer to the endpoints (`low` and `high`).

    if `a` and `b` are different then it will shift closer to the `low` or `high`
    """
    return low + (high - low) * betavariate(a, b)


def get_even_curved_num(low: float, high: float, curve: float = 5) -> float:
    """Get a random number that is between low and high.

    if `curve=1` then it is equal chance for all numbers between `low` and `high`.

    if `curve>1`, it becomes closer to the average of `low` and `high`.

    if `curve<1`, it becomes closer to the endpoints (`low` and `high`).
    """
    return get_curved_num(low, high, curve, curve)


def get_left_curved_num(low: float, high: float, curve: float = 5) -> float:
    """Get a random number that is between low and high.

    if `curve=1` then it is equal chance for all numbers between `low` and `high`.

    if `curve<1`, it becomes closer to `low` and farther from `high`.
    """
    return get_curved_num(low, high, 1, curve)


def get_right_curved_num(low: float, high: float, curve: float = 5) -> float:
    """Get a random number that is between low and high.

    if `curve=1` then it is equal chance for all numbers between `low` and `high`.

    if `curve<1`, it becomes closer to `high` and farther from `low`.
    """
    return get_curved_num(low, high, curve, 1)


def get_curve_mean(low: float, high: float, a: float, b: float) -> float:
    return ((a - 1) / (a + b - 2)) * (high - low) + low


def get_with_mean(mean: float, low: float, high: float, a: float, b: float) -> float:
    return get_curved_num((mean + low) / 2, high, a, b)
