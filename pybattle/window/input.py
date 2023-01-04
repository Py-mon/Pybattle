from typing import Callable

from pybattle.ansi.colors import Colors
from pybattle.types_ import CoordReference, SizeReference
from pybattle.window.coord import Coord
from pybattle.window.frames.center_frame import CenteredFrame
from pybattle.window.frames.frame import Frame
from pybattle.window.matrix import Matrix
from pybattle.window.size import Size


class Selection:
    def __init__(self, label: str, location: CoordReference, size: SizeReference = ...) -> None:
        self.location = Coord(location)
        self.size = Size(size)
        self.label = label


class SelectionMenu:
    def __init__(
        self, 
        size: SizeReference,
        selections: list[Selection],
        default_color: str = Colors.GRAY
    ) -> None:
        self.selections = selections
        
        self.selection = selections[0]
        
        self.frame = Frame(size)
        
        for selection in self.selections:
            if selection == self.selection:
                self.frame.add_frame(CenteredFrame(selection.size, selection.label), selection.location)
            else:
                self.frame.add_frame(CenteredFrame(Matrix(selection.label, (0, default_color)), selection.size), selection.location)  
  
def func(p1, p2):
    x1, x2 = p1
    y1, y2 = p2
    
    if abs(x2-x1) > abs(y2-y1):
        if x1 > x2:
            return 'right'
        else:
            return 'left'
    else:
        if y1 > y2:
            return 'up'
        else:
            return 'down'
            
print(func((0, 0), (3,4)))
