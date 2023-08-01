from itertools import chain

from pybattle.screen.grid.cell import Cell
from pybattle.types_ import Alignment
from typing import Self


def is_nested(seq: list | list[list]) -> bool:
    """Check if a sequence is nested"""
    return len(seq) > 0 and isinstance(seq[0], (list, str))


def nested_len(seq: list[list] | list[str]) -> int:
    """Get the max nested length of a list. If not nested returns the length."""
    return max([len(row) for row in seq] + [0])


def nest(seq: list) -> list[list]:
    """If a sequence is not nested, it returns it nested"""
    if is_nested(seq):
        return seq
    return [seq]


def flatten(nested_list: list[list]) -> list:
    return list(chain(*nested_list))


def format_list(lst):
    def format(lst, join_):
        if not isinstance(lst, list):
            return str(lst)

        elements = []
        for item in lst:
            elements.append(format(item, ","))

        return "[" + (join_).join(elements) + "]"

    if is_nested(lst):
        return format(lst, ",\n ")
    return format(lst, ",")



def level_out(rows: list[list], alignment: Alignment = Alignment.LEFT):
    """Level out the rows of the matrix making them all the same width"""

    if rows:
        max_length = nested_len(rows)

        for row in rows:
            row_length = len(row)
            if row_length >= max_length:
                continue

            match alignment:
                case Alignment.LEFT:
                    row.extend(Cell(" ") * (max_length - row_length))
                case Alignment.RIGHT:
                    for _ in range(max_length - row_length):
                        row.insert(0, Cell(" "))
                case Alignment.CENTER:
                    left_padding = (max_length - row_length) // 2
                    right_padding = max_length - row_length - left_padding
                    row[:] = (
                        [Cell(" ")] * left_padding + row + [Cell(" ")] * right_padding
                    )
