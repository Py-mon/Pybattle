from typing import Callable

from src.types_ import CoordReference, SizeReference
from src.window.coord import Coord
from src.window.frame import Window
from src.window.color import Color
from src.window.size import Size


class Selection:
    def __init__(self, location: CoordReference, action: Callable[[], None]) -> None:
        self.location = Coord.convert_reference(location)
        self.action = action
        
    def use(self, location: CoordReference) -> None:
        if  Coord.convert_reference(location) == self.location:
            self.action()


class SelectionMenu:
    # TODO: Finish with new color matrix
    def __init__(
        self, size: SizeReference,
        selections: dict[str, (CoordReference, SizeReference)],
        default_color: str = Color.GRAY
    ) -> None:
        for coord in selections:
            selections[coord] = Coord.convert_reference(selections[coord])
        self.selections = selections
        
        self.selection = list(selections.keys())[0]
        
        # TODO: Add color on current selection
        
        self.frame = Window(size=size)
        for selection, (location, size) in self.selections.items():
            size = Size.convert_reference(size)
            if selection == self.selection:
                if size is not None:
                    self.frame.add_frame(Window(selection, size), location)
                else:
                    self.frame.add_frame(Window(selection), location)
            else:
                if size is not None:
                    self.frame.add_frame(Window(selection, size), location)
                else:
                    self.frame.add_frame(Window(selection), location)


SelectionMenu((15, 15), {'a': ((1, 1), (3, 5)), 'b': ((4, 4), None), 'c': ((9, 9), None)})
  
  
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
