from typing_extensions import Protocol
from typing import Generic

class Proto(Protocol):
    def __init__(self, bar: str):
        self.bar: str


class Foo:
    def __init__(self, bar: str | int):
        self.bar = bar

    def __class_getitem__(cls, item):
        return Proto


x = Foo
y: x = Foo("Hello, World!")
