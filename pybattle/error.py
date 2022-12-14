from pybattle.traceback import Traceback


class Error(Exception):
    """The base traceback error."""
    def __init__(self, msg, traceback: bool = True) -> None:
        self.msg = msg
        
        if traceback:
            self.traceback = Traceback()
        else:
            self.traceback = None

    def __str__(self) -> str:
        if self.traceback is None:
            return self.msg
        return self.traceback.trace + ' ' + self.msg


class OutOfBoundsError(Error):
    """Coords out of bounds."""
    pass


class InsufficientArgumentsError(Error):
    """Too few arguments required."""
    pass