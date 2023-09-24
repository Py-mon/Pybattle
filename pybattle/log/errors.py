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
    """Out of bounds of certain size range."""


class MethodDoesNotExist(Error, NotImplementedError, AttributeError):
    """Attribute not found or not implemented."""


class TooSmallError(Error, ValueError):
    """too small"""


class AttributeMissing(Error, AttributeError):
    """Cannot do because there is no attribute."""
