import logging
from inspect import getframeinfo, stack
from pathlib import Path
from os import mkdir


def get_logger(level: int = logging.DEBUG, file_name: str = ...) -> logging.Logger:
    """Get or creates a logger named the file."""
    if file_name == ...:
        file_name = getframeinfo(stack()[1][0]).filename  # The file path

    # ...\tester.py -> tester
    # tester.py -> tester
    # tester -> tester
    name = Path(file_name).stem
    
    logger = logging.getLogger(name)

    try:
        mkdir(r'Loggers')
    except FileExistsError:
        pass

    if not logger.handlers:  # If logger has been created (it has no handlers)
        logger.setLevel(level)
        
        handler = logging.FileHandler(r'Loggers\\' + name + '.log', mode='w')
        formatter = logging.Formatter(
            "%(levelname)s: %(message)s")  # LEVEL: message

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
