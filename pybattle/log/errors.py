from typing import Callable, Optional, Type

from pybattle.log.log import logger


class Error(Exception):
    """The base Error class that logs the errors with the level `ERROR`"""

    def __init__(self, msg: str = "", add_stack_level: int = 0) -> None:
        self.message = f"{type(self).__name__}: {msg}"
        logger.error(self.message, stack_level=add_stack_level + 3)
        super().__init__(self.message)

# Adding a secondary inheritances catches errors under those types
class OutOfBounds(Error, IndexError):
    """`x` out of bounds of `y` by `z`"""

    def __init__(self, out, bounds) -> None:
        super().__init__(f"{out} is out of bounds of {bounds} by {out + 1 - bounds}", 1)


class MethodDoesNotExist(Error, NotImplementedError):
    """Method `x` does not exist for `y`"""

    def __init__(self, method: Callable, for_: Optional[Type] = None) -> None:
        msg = f"Method '{method.__name__}' does not exist"
        if for_ is not None:
            msg += " for " + for_.__name__
        super().__init__(msg, 1)


class SizeTooSmall(Error, ValueError):
    """`x` is too small for `y`"""

    def __init__(self, too_small: object, for_: str) -> None:
        super().__init__(f"{too_small} is too small for {for_}", 1)


class InvalidConvertType(Error, ValueError):
    """Unable to convert type `x` to type `y`"""

    def __init__(self, invalid: Type, to: Type) -> None:
        super().__init__(
            f"Unable to convert '{invalid.__name__}' to '{to.__name__}'", 1
        )
