from pybattle.window.grid.matrix import Matrix
from pybattle.window.grid.coord import Coord
from pybattle.window.frames.map_frame import MapFrame


class Camera:
    def __init__(self, text, range_) -> None:
        self.matrix = Matrix(text)
        self.range_ = range_
        
    def camera(self, pos):
        return self.matrix[pos - self.range_: min(self.matrix.size - 1, pos + self.range_)].text
