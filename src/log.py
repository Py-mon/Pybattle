from inspect import stack
from logging import DEBUG, FileHandler, Formatter, getLogger
from pathlib import Path


class Traceback:
    """Show information like the file, line, or line number of a log."""

    def __init__(self):
        """
        ```
        stack()[0] -> "Info About this line"
        stack()[1] -> "About the line it is used"
        ...
        ```
        """
        # Get the latest traceback
        n = 0
        while True:
            try:
                self.filename = stack()[n].filename
                self.line_num = stack()[n].lineno
                self.line = stack()[n].code_context[0].rstrip('\n')
                n += 1
            except:
                self.filename = stack()[n - 1].filename
                self.line_num = stack()[n - 1].lineno
                self.line = stack()[n - 1].code_context[0].rstrip('\n')
                break

    @property
    def trace(self):
        # TODO: Show where one the line the log came from
        return f'''\
In file {self.filename} on line {self.line_num}
{self.line}\n'''


class Logger:
    logger = getLogger('log')

    logger.setLevel(DEBUG)

    __handler = FileHandler(Path('log.log'), mode='w')
    __formatter = Formatter(
        "%(levelname)s: %(message)s")  # LEVEL: message

    __handler.setFormatter(__formatter)

    logger.addHandler(__handler)

    @classmethod
    def debug(cls, msg: str, traceback: bool = False) -> None:
        if traceback:
            cls.logger.debug(Traceback().trace + msg)
        else:
            cls.logger.debug(msg)

    @classmethod
    def warning(cls, msg: str, traceback: bool = True) -> None:
        if traceback:
            cls.logger.warning(Traceback().trace + msg)
        else:
            cls.logger.warning(msg)

    @classmethod
    def info(cls, msg: str, traceback: bool = False) -> None:
        if traceback:
            cls.logger.info(Traceback().trace + msg)
        else:
            cls.logger.info(msg)
