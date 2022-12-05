from logging import DEBUG, FileHandler, Formatter, getLogger
from pathlib import Path
from src.types_ import Error
from src.traceback import Traceback


class Logger:
    logger = getLogger('log')

    logger.setLevel(DEBUG)

    __handler = FileHandler(Path('log.log'), mode='w')
    __formatter = Formatter(
        "%(levelname)s: %(message)s")  # LEVEL: message

    __handler.setFormatter(__formatter)

    logger.addHandler(__handler)
    
    @classmethod
    def error(cls, msg: str, error: Error = Error, traceback: bool = True) -> None:
        if traceback:
            cls.logger.error(Traceback().trace + msg)
        else:
            cls.logger.error(msg)
        raise error(msg)

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
