class Error(Exception):
    """The base traceback error."""
    pass


class OutOfBoundsError(Error, IndexError):
    """Coords out of bounds."""
    pass


class InsufficientArgumentsError(Error, TypeError):
    """Not enough arguments required."""
    pass


class InvalidMethodError(Error, NameError):
    """Invalid method."""
    pass
