from inspect import stack


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
