from typing import Callable, Optional, Type

from pybattle.log.log import logger


class Error(Exception):
    """The base Error class that logs the errors with the level `ERROR`"""

    add_stack_level: int = 0

    def __init__(self, msg: str = "") -> None:
        self.message = (
            f"{type(self).__name__}{':' if [char != ' ' for char in msg] else ''} {msg}"
        )
        logger.error(self.message, stack_level=type(self).add_stack_level + 3)
        super().__init__(msg)

    def __init_subclass__(cls) -> None:
        cls.add_stack_level += 1
        return super().__init_subclass__()


class OutOfBounds(Error, IndexError):
    """`x` out of bounds of `y` by `z`"""

    def __init__(self, out, bounds) -> None:
        super().__init__(f"{out} is out of bounds of {bounds} by {out + 1 - bounds}")


class MethodDoesNotExist(Error, NotImplementedError):
    """Method `x` does not exist for `y`"""

    def __init__(self, method: Callable, for_: Optional[Type] = None) -> None:
        msg = f"Method '{method.__name__}' does not exist"
        if for_ is not None:
            msg += " for " + for_.__name__
        super().__init__(msg)


class SizeTooSmall(Error, ValueError):
    """`x` is too small for `y`"""

    def __init__(self, too_small: object, for_: str) -> None:
        super().__init__(f"{too_small} is too small for {for_}")


class NegativeError(Error, ValueError):
    """Negatives (`y`) are invalid for `x`"""

    def __init__(self, numbers: dict[str, int], for_: Type) -> None:
        super().__init__(
            f"Negatives ({', '.join([repr(name) + ': ' + str(neg) for name, neg in numbers.items() if neg < 0])}) are invalid for '{for_.__name__}'s",
        )
