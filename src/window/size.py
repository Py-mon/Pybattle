"""2D (Width, Height)"""

from typing import Self, Sequence

from src.types_ import SizeReference


class Size:
    """2D (Width, Height)"""

    def __init__(
        self,
        height: int,
        width: int
    ) -> None:
        self.width = width
        self.height = height

    @staticmethod
    def convert_reference(reference: SizeReference) -> "Size":  # Says Any with Self (due to staticmethod)
        if isinstance(reference, int):
            return Size(reference, reference)
        if isinstance(reference, tuple):
            return Size(*reference)
        return reference

    @property
    def size(self) -> tuple[int, int]:
        return (self.height, self.width)

    def add(self, other: SizeReference) -> Self:
        other = Size.convert_reference(other)
        return Size(self.width + other.width, self.height + other.height)

    def subtract(self, other: SizeReference) -> Self:
        other = Size.convert_reference(other)
        return Size(self.width - other.width, self.height - other.height)

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
    
    def __contains__(self, sequence: Sequence[SizeReference]) -> bool:
        for size in sequence:
            size = Size.convert_reference(size)
            if self.width == size.width and self.height == size.height:
                return True
        return False

    def __repr__(self) -> str:
        return f'(Height: {self.height}, Width: {self.width})'
