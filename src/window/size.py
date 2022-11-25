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
        if isinstance(reference, tuple):
            return Size(*reference)
        return reference

    @property
    def size(self) -> tuple[int, int]:
        return self.height, self.width
    
    def __iter__(self):
        return iter(self.size)

    def __repr__(self) -> str:
        return f'(Height: {self.height}, Width: {self.width})'
