from inspect import stack
from logging import DEBUG, FileHandler, Formatter, getLogger, Logger
from pathlib import Path
from typing import Optional


class Traceback:
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


logger = getLogger('log')

logger.setLevel(DEBUG)

__handler = FileHandler(Path('log.log'), mode='w')
__formatter = Formatter(
    "%(levelname)s: %(message)s")  # LEVEL: message

__handler.setFormatter(__formatter)

logger.addHandler(__handler)


class _Logger:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def debug(self, msg: str, traceback: bool = False) -> None:
        if traceback:
            self.logger.debug(Traceback().trace + msg)
        else:
            self.logger.debug(msg)

    def warning(self, msg: str, traceback: bool = True) -> None:
        if traceback:
            self.logger.warning(Traceback().trace + msg)
        else:
            self.logger.warning(msg)

    def info(self, msg: str, traceback: bool = True) -> None:
        if traceback:
            self.logger.info(Traceback().trace + msg)
        else:
            self.logger.info(msg)


logger = _Logger(logger)
