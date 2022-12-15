
from typing import Self, Sequence

from pybattle.types_ import SizeReference


class Size:
    """2D (Height, Width)"""

    def __init__(
        self,
        height: int,
        width: int
    ) -> None:
        self.width = width
        self.height = height

    @staticmethod
    def convert_reference(reference: SizeReference) -> "Size":
        """
        ```
        Size(5, 5) -> Size(5, 5)
        (1, 3) -> Size(1, 3)
        ... -> ...
        """
        if isinstance(reference, int):
            return Size(reference, reference)
        if isinstance(reference, tuple):
            return Size(*reference)
        return reference

    @property
    def size(self) -> tuple[int, int]:
        return (self.height, self.width)
    
    @property
    def center(self) -> Self:
        height = self.height // 2
        width = self.width // 2
        if height == 0:
            height = self.height
        if width == 0:
            width = self.width
            
        return Size(height, width)

    @property
    def reverse(self) -> tuple[int, int]:
        return (self.width, self.height)

    def add(self, other: SizeReference) -> Self:
        other = Size.convert_reference(other)
        return Size(self.height + other.height, self.width + other.width)

    def subtract(self, other: SizeReference) -> Self:
        other = Size.convert_reference(other)
        return Size(self.height - other.height, self.width - other.width)

    def __add__(self, other: SizeReference) -> Self:
        return self.add(other)

    def __iadd__(self, other: SizeReference) -> Self:
        return self.add(other)

    def __sub__(self, other: SizeReference) -> Self:
        return self.subtract(other)

    def __isub__(self, other: SizeReference) -> Self:
        return self.subtract(other)

    def __iter__(self):
        return iter(self.size)

    def __eq__(self, other: SizeReference) -> bool:
        other = Size.convert_reference(other)
        if self.width == other.width and self.height == other.height:
            return True
        return False

    def __repr__(self) -> str:
        return f'(Height: {self.height}, Width: {self.width})'
