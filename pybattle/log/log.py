from logging import (
    DEBUG,
    FileHandler,
    Formatter,
    Filter,
    LogRecord,
    Logger,
)
from pathlib import Path
from traceback import format_stack
import datetime


LEVEL = DEBUG

ON = []
OFF = []

NAME = "log"
FILE = "logs/log.log"

MICRO_PLACES = 2

FORMAT = """Traceback (most recent call last):\n%(traceback)s%(levelname)s at %(time)s: %(message)s"""


class TracebackLogger(Logger):
    def __init__(self, name: str, level=DEBUG) -> None:
        super().__init__(name, level)
        self.stack_level = 1
        self.error = self._with_stack_level(self.error, 4)

    def _with_stack_level(self, func, level: int):
        def wrapper(*args, **kwargs):
            self.stack_level = level
            func(*args, **kwargs)
            self.stack_level = 1

        return wrapper

    def warning(self, msg, *args, stack_info=True, **kwargs):
        super().warning(msg, *args, stack_info=stack_info, **kwargs)

    def error(self, msg, *args, stack_level: int = 1, stack_info=True, **kwargs):
        self.stack_level = stack_level
        super().error(msg, *args, stack_info=stack_info, **kwargs)
        self.stack_level = 1

    def critical(self, msg, *args, stack_info=True, **kwargs):
        super().critical(msg, *args, stack_info=stack_info, **kwargs)


logger = TracebackLogger(NAME, LEVEL)


class LogFilter(Filter):
    def __init__(self, on: list[str], off: list[str], micro_places: int = 2):
        super().__init__()

        self.on = on
        self.off = off
        self.micro_places = micro_places

    def filter(self, record: LogRecord):
        record.traceback = ""
        if record.stack_info is not None:
            record.traceback = "\n".join(format_stack()[: -4 - logger.stack_level])
            record.stack_info = None

        # HH:MM:SS,mm
        time = datetime.datetime.today()
        microsecond = format(time.microsecond, "06d")[: self.micro_places]
        record.time = time.strftime(f"%H:%M:%S,{microsecond}")

        if not self.on and not self.off:
            return True

        for module in self.on:
            if module in Path(record.pathname).parts:
                return True

        for module in self.off:
            if module not in Path(record.pathname).parts:
                return True

        return False


__handler = FileHandler(FILE, mode="w", encoding="utf-8")
__handler.setFormatter(Formatter(FORMAT))
logger.addHandler(__handler)

logger.addFilter(LogFilter(ON, OFF, MICRO_PLACES))
