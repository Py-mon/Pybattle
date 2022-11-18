from logging import getLogger, FileHandler, Formatter, DEBUG
from inspect import getframeinfo, stack
from pathlib import Path
from os import mkdir


class FileLogger:
    """A logger for a file. When you log it also goes into a global log file."""
    try:
        mkdir('Loggers')
    except FileExistsError:
        pass
    
    global_logger = getLogger('global')
    
    global_logger.setLevel(DEBUG)

    __handler = FileHandler(Path('Loggers/global.log'), mode='w')
    __formatter = Formatter(
        "%(levelname)s: %(message)s")  # LEVEL: message

    __handler.setFormatter(__formatter)

    global_logger.addHandler(__handler)
    
    def __init__(self, file_name: str = ..., default_level: int = DEBUG) -> None:
        if file_name == ...:
            file_name = getframeinfo(stack()[1][0]).filename  # The file path
        self.default_level = default_level

        # ...\tester.py -> tester
        # tester.py -> tester
        # tester -> tester
        name = Path(file_name).stem

        logger = getLogger(name)

        if not logger.hasHandlers():  # If logger has been created (it has no handlers)
            logger.setLevel(default_level)
            
            handler = FileHandler(Path('Loggers/' + name + '.log'), mode='w')
            formatter = Formatter(
                "%(levelname)s: %(message)s")  # LEVEL: message

            handler.setFormatter(formatter)

            logger.addHandler(handler)
        
        self.logger = logger
    
    def log(self, msg: str, level: int = ...) -> None:
        if level is ...:
            level = self.default_level
        self.logger.log(level, msg)
        self.global_logger.log(level, msg)
        
    def debug(self, msg: str) -> None:
        self.logger.debug(msg)
        self.global_logger.debug(msg)
        
    def warning(self, msg: str) -> None:
        self.logger.warning(msg)
        self.global_logger.warning(msg)
        
    def info(self, msg: str) -> None:
        self.logger.info(msg)
        self.global_logger.info(msg)
