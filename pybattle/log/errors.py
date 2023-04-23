from pybattle.log.log import logger
from typing import Type, Callable, Optional


class Error(Exception):
    """The base logged error (Add a secondary inheritances to catch errors under those types)"""

    def __init__(self, msg: str = "", stack_level: int = 1) -> None:
        self.message = f"{type(self).__name__}: {msg}"
        logger.error(self.message, stack_level=stack_level + 3)
        super().__init__(self.message)


class OutOfBounds(Error, IndexError):
    """x out of bounds of y by z"""

    def __init__(self, out, bounds) -> None:
        super().__init__(f"{out} is out of bounds of {bounds} by {out - bounds}", 2)


class MethodDoesNotExist(Error, NotImplementedError):
    """Method 'x' does not exist for y"""

    def __init__(self, method: Callable, for_: Optional[Type] = None) -> None:
        msg = f"Method '{method.__name__}' does not exist"
        if for_ is not None:
            msg += " for " + for_.__name__
        super().__init__(msg, 2)


class SizeTooSmall(Error, ValueError):
    """x is too small for y"""

    def __init__(self, too_small: object, for_: str) -> None:
        super().__init__(f"{too_small} is too small for {for_}", 2)


class InvalidConvertType(Error, ValueError):
    """Unable to convert type 'x' to type 'y'"""

    def __init__(self, invalid: Type, to: Type) -> None:
        super().__init__(
            f"Unable to convert '{invalid.__name__}' to '{to.__name__}'", 2
        )
