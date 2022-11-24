from typing import Self
from source.types_ import SizeReference


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
    def convert_reference(reference: SizeReference) -> "Size":
        if isinstance(reference, tuple):
            return Size(*reference)
        return reference

    @property
    def size(self) -> Self:
        return Size(self.height, self.width)

    def __repr__(self) -> str:
        return f'(Height: {self.height}, Width: {self.width})'
