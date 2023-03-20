import traceback
from re import search


class Traceback:
    def __init__(self):
        self.stack = traceback.format_stack()
        self.source = "".join(self.stack[-2])
        self.traceback = "".join(self.stack[:-2])


def find_file(source: str) -> str:
    match = search(r'File "([^"]+)", line (\d+)(?:, in (\S+))?\n\s+(.+)', source)

    if match:
        return match.group(1)
    else:
        raise TypeError(f'Invalid Source: {source}')

    # self.line_number = match.group(2)
    # self.line = match.group(3)
