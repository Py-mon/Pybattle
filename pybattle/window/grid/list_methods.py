def is_nested(lst: list | list[list]) -> bool:
    """Check if a list is nested"""
    return len(lst) > 0 and isinstance(lst[0], list)


def nested_len(lst: list | list[list]) -> int:
    """Get the max nested length of a list. If not nested returns the length."""
    if is_nested(lst):
        return max([len(row) for row in lst] + [0])
    return len(lst)
