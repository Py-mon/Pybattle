from typing import Callable

from src.types_ import CoordReference, SizeReference
from src.window.coord import Coord
from src.window.frame import Window
from src.window.color import Colors
from src.window.size import Size


class Selection:
    def __init__(self, label: str, location: CoordReference, size: SizeReference = ...) -> None:
        self.location = Coord.convert_reference(location)
        self.size = Size.convert_reference(size)
        self.label = label


class SelectionMenu:
    # TODO: Finish with new color matrix
    def __init__(
        self, size: SizeReference,
        selections: list[Selection],
        default_color: str = Colors.GRAY
    ) -> None:
        self.selections = selections
        
        self.selection = selections[0]
        
        self.frame = Window(size=size)
        for selection in self.selections:
            if selection == self.selection:
                # TODO: Add color using default_color (Need to fix matrix)
                self.frame.add_frame(Window(selection.label, selection.size), selection.location)
            else:
                self.frame.add_frame(Window(str(default_color) + selection.label, selection.size), selection.location)


SelectionMenu((15, 15), [Selection('a', (1, 1), (3, 5)), Selection('b', (4, 4)), Selection('c', (8, 8))])
  
  
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
