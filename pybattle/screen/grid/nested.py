from itertools import chain
from typing import Self

from pybattle.screen.grid.cell import Cell
from pybattle.types_ import Alignment


def is_nested(seq: list | list[list]) -> bool:
    """Check if a sequence is nested"""
    return len(seq) > 0 and isinstance(seq[0], (list, str, tuple))


def max_len(seq: tuple[tuple, ...] | tuple[str, ...] | list[str]) -> int:
    """Get the max length of row in a nested list."""
    return max([len(row) for row in seq] + [0])


def nest(seq: list) -> list[list]:
    """If a sequence is not nested, it returns it nested"""
    if is_nested(seq):
        return seq
    return [seq]


def flatten(nested_list: list[list]) -> list:
    return list(chain(*nested_list))


def format(tup):
    def format_(tup_, join_):
        if not isinstance(tup_, tuple):
            return repr(tup_)

        elements = []
        for item in tup_:
            elements.append(format_(item, ","))

        return "(" + (join_).join(elements) + ")"

    if is_nested(tup):
        return format_(tup, ",\n ")
    return format_(tup, ",")


def level_out(
    rows: tuple[tuple], alignment: Alignment = Alignment.LEFT
) -> tuple[tuple, ...]:
    """Level out the rows of the matrix making them all the same width"""
    max_length = max(len(row) for row in rows)

    new_rows = []
    for row in rows:
        row_length = len(row)
        if row_length >= max_length:
            new_rows.append(row)
            continue
        
        if alignment == Alignment.LEFT:
            new_row = row + (Cell(" "),) * (max_length - row_length)
        elif alignment == Alignment.RIGHT:
            new_row = (Cell(" "),) * (max_length - row_length) + row
        elif alignment == Alignment.CENTER:
            left_padding = (max_length - row_length) // 2
            right_padding = max_length - row_length - left_padding
            new_row = (Cell(" "),) * left_padding + row + (Cell(" "),) * right_padding
        else:
            raise ValueError

        new_rows.append(new_row)

    return tuple(new_rows)
