import datetime
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    WARNING,
    FileHandler,
    Filter,
    Formatter,
    Logger,
    LogRecord,
)
from pathlib import Path
from traceback import format_stack

from toml import load

with open("logs/logging.toml") as t:
    conf = load(t)


LEVEL = eval(
    conf["logger"]["level"],
    {
        "DEBUG": DEBUG,
        "ERROR": ERROR,
        "FATAL": FATAL,
        "INFO": INFO,
        "CRITICAL": CRITICAL,
        "WARNING": WARNING,
    },
)

ON = set(conf["filter"]["on"])
OFF = set(conf["filter"]["off"])

NAME = conf["logger"]["name"]
FILE = conf["logger"]["file"]

MICRO_PLACES = conf["time"]["micro_places"]

FORMAT = conf["logger"]["format"]


class _TracebackLogger(Logger):
    """
    - Unique traceback format
    - Different defaults for the logging methods
    - Displays the time in `HH:MM:SS,mm`"""

    def __init__(self, name: str, level=DEBUG, micro_places: int = 2) -> None:
        super().__init__(name, level)
        self.stack_level = 2
        self.micro_places = micro_places

    def _get_extras(self, traceback: bool = True, stack_level: int = ...):
        if stack_level is not ...:
            self.stack_level = stack_level

        traceback_info = ""
        if traceback:
            traceback_info = "\nTraceback (most recent call last):\n" + "\n".join(
                format_stack()[: -logger.stack_level]  # -4 -3
            )

        # HH:MM:SS,mm
        time = datetime.datetime.today()
        microsecond = format(time.microsecond, "06d")[: self.micro_places]
        time = time.strftime(f"%H:%M:%S,{microsecond}")

        return {
            "stack_level": self.stack_level,
            "traceback": traceback_info,
            "time": time,
        }

    def log(self, msg, traceback: bool = False, stack_level: int = ...):
        super().debug(
            msg,
            extra=self._get_extras(traceback, stack_level),
        )

    def debug(self, msg, traceback: bool = False, stack_level: int = ...):
        super().debug(
            msg,
            extra=self._get_extras(traceback, stack_level),
        )

    def warning(self, msg, traceback: bool = True, stack_level: int = ...):
        super().warning(
            msg,
            extra=self._get_extras(traceback, stack_level),
        )

    def error(self, msg, traceback: bool = True, stack_level: int = ...):
        super().error(
            msg,
            extra=self._get_extras(traceback, stack_level),
        )

    def critical(self, msg, traceback: bool = True, stack_level: int = ...):
        super().critical(
            msg,
            extra=self._get_extras(traceback, stack_level),
        )


class _LogFilter(Filter):
    """Filters on and off the logs depending on the file."""

    def __init__(self, on: set[str], off: set[str]):
        super().__init__()

        self.on = on
        self.off = off

    def filter(self, record: LogRecord):
        if not self.on or not self.off:
            return True

        parts = set(Path(record.pathname).parts)

        return (parts & self.on) or (not (parts & self.off))


def _create_logger():
    logger = _TracebackLogger(NAME, LEVEL, MICRO_PLACES)

    handler = FileHandler(FILE, mode="w", encoding="utf-8")
    handler.setFormatter(Formatter(FORMAT))
    logger.addHandler(handler)

    logger.addFilter(_LogFilter(ON, OFF))

    return logger


logger = _create_logger()
