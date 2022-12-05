from src.log import Traceback


class Error(Exception):
    def __init__(self, msg, traceback: bool = True) -> None:
        self.msg = msg

        self.traceback = traceback
        if self.traceback:
            self.traceback = Traceback()

    def __str__(self) -> str:
        return self.traceback.trace + ' ' + self.msg


class OutOfBoundsError(Error):
    pass

