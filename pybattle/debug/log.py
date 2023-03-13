from logging import DEBUG, FileHandler, Formatter, getLogger
from pathlib import Path
from pybattle.debug.traceback import Traceback
from pybattle.debug.errors import Error
from typing import Type


class Logger:
    logger = getLogger('log')

    logger.setLevel(DEBUG)

    __handler = FileHandler(Path('log.log'), mode='w', encoding="utf-8")
    __formatter = Formatter(
        "%(levelname)s: %(message)s")  # LEVEL: message

    __handler.setFormatter(__formatter)

    logger.addHandler(__handler)
    
    @classmethod
    def error(cls, msg: str = '', error: Type[Error] = Error, traceback: bool = True) -> None:
        if traceback:
            cls.logger.error(f'{Traceback().trace} {error.__name__}: {msg}')
        else:
            cls.logger.error(error.__name__ + ': ' + msg)
        raise error(msg)

    @classmethod
    def debug(cls, msg: str, traceback: bool = False) -> None:
        if traceback:
            cls.logger.debug(Traceback().trace + msg)
        else:
            cls.logger.debug(msg)
            
    @classmethod
    def info_debug(cls, msg: str) -> None:
        cls.logger.debug(f'Log from: {Traceback(1).trace}{msg}')

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
