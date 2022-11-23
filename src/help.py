from typing import Callable, Any
from inspect import getfullargspec


# Prints info of any function in format: function(arg1, arg2, arg3, ...)
def function_info(func: Callable[[..., Any], Any]):
    args = ', '.join(getfullargspec(func).args)
    return f'{func.__name__}({args})'