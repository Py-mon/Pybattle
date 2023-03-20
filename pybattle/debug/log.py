from logging import DEBUG, FileHandler, Formatter, getLogger
from pathlib import Path
from typing import Type

from pybattle.debug.errors import Error
from pybattle.debug.traceback_ import Traceback, find_file


class Logger:
    LEVEL = DEBUG
    FILTERED = []
    
    logger = getLogger('log')

    logger.setLevel(LEVEL)

    __handler = FileHandler(Path('log.log'), mode='w', encoding="utf-8")
    __formatter = Formatter(
        "%(levelname)s: %(message)s")  # LEVEL: message

    __handler.setFormatter(__formatter)

    logger.addHandler(__handler)
    
    @classmethod
    def file_check(cls) -> bool:
        if not cls.FILTERED:
            return True
        for module in cls.FILTERED:
            for traceback in Traceback().stack[:-3]:
                traceback_file = find_file(traceback)
                print(Path(module).name, Path(traceback_file).name)
                print(Path(traceback_file).parent)
                if Path(module).name == Path(traceback_file).name:
                    return True
                
                traceback_dir = Path(traceback_file)
                while traceback_dir != traceback_dir.parent:
                    traceback_dir = traceback_dir.parent
                    print(repr(traceback_dir))
                    if Path(module).name == traceback_dir.name:
                        return True
        else:
            return False
    
    @classmethod
    def error(cls, msg: str = '', error: Type[Error] = Error, traceback: bool = True) -> None:
        if traceback:
            cls.logger.error(f'\n{Traceback().traceback}{error.__name__}: {msg}')
        else:
            cls.logger.error(error.__name__ + ': ' + msg)
        raise error(msg)

    @classmethod
    def debug(cls, msg: str, traceback: bool = False) -> None:
        if cls.file_check():
            if traceback:
                cls.logger.debug(f"\n{Traceback().traceback}{msg}")
            else:
                prefix = "\n" if "\n" in msg else ""
                cls.logger.debug(f"{prefix}{msg}")
            
    @classmethod
    def trace_debug(cls, msg: str) -> None:
        cls.debug(msg, traceback=True)

    @classmethod
    def warning(cls, msg: str, traceback: bool = True) -> None:
        if cls.file_check():
            if traceback:
                cls.logger.warning(f'\n{Traceback().traceback}{msg}')
            else:
                prefix = "\n" if "\n" in msg else ""
                cls.logger.warning(f"{prefix}{msg}")
            
    @classmethod
    def info(cls, msg: str, traceback: bool = False) -> None:
        if cls.file_check():
            if traceback:
                cls.logger.info(f'\n{Traceback().traceback}{msg}')
            else:
                prefix = "\n" if "\n" in msg else ""
                cls.logger.warning(f"{prefix}{msg}")
            
