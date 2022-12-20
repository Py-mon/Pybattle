from pybattle.window.coord import Coord
from pybattle.window.range import Range


class Size(Coord, Range):
    def __init__(self, height: int, width: int) -> None:
        Coord.__init__(self, height, width)
        Range.__init__(self, self.coords)

    @property
    def height(self) -> int:
        return self.y

    @property
    def width(self) -> int:
        return self.x
    
    @property
    def inner_height(self) -> int:
        return self.height - 2
    
    @property
    def inner_width(self) -> int:
        return self.width - 2

    def __repr__(self) -> str:
        return f'Size(height={self.height}, width={self.width})'
