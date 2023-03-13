from typing import Literal

from pybattle.ansi.colors import ColorType
from pybattle.types_ import CoordReference, SizeReference
from pybattle.window.grid.coord import Coord
from pybattle.window.frames.center_frame import CenteredFrame
from pybattle.window.frames.frame3 import Frame
from pybattle.window.grid.matrix import Matrix
from pybattle.window.grid.size import Size
from pybattle.ansi.screen import Screen
from keyboard import is_pressed


def func(coord: Coord, compare_coord: Coord) -> Literal['right', 'left', 'up', 'down', 'equal']:
    y1, x1 = coord
    y2, x2 = compare_coord
    
    if abs(x2 - x1) > abs(y2 - y1):
        if x1 > x2:
            return 'left'
        else:
            return 'right'
    else:
        if y1 > y2:
            return 'up'
        elif y1 == y2:
            return 'equal'
        else:
            return 'down'


class Selection:
    def __init__(self, label: str, location: CoordReference, size: SizeReference = ...) -> None:
        self.location = Coord(location)
        self.label = label
        
        self.size = Size(size)
        if self.size is ...:
            self.size = Size(label) - 1
    
    def __repr__(self):
        return str(self.location)


class SelectionMenu:
    def __init__(
        self, 
        size: SizeReference,
        selections: list[Selection],
        default_color: ColorType = ColorType.BLUE
    ) -> None:
        self.default_color = default_color
        self.selections = selections
        
        self.selection = selections[0]
        
        self._frame = Frame(size)

    @property
    def frame(self):
        for selection in self.selections:
            if selection == self.selection:
                self._frame.add_frame(CenteredFrame(selection.size, Matrix(selection.label, ((0, 0), self.default_color))), selection.location)
            else:
                self._frame.add_frame(CenteredFrame(selection.size, selection.label), selection.location)
        return self._frame
    
    @property
    def directions(self) -> list[str]:
        return [func(self.selection.location, location.location) for location in self.selections]

    def move(self, direction: Literal['right', 'left', 'up', 'down']) -> None:
        if direction in self.directions:
            selection_index = self.directions.index('equal')
            if direction in self.directions[:selection_index]:
                index = self.directions.index(direction, selection_index - 1)
            else:
                index = self.directions.index(direction)
                
            self.selection = self.selections[index]

    def right(self) -> None:
        self.move('right')

    def left(self) -> None:
        self.move('left')
        
    def up(self) -> None:
        self.move('up')
        
    def down(self) -> None:
        self.move('down')

    def loop(self) -> None:
        while True:
            Screen.write(self.frame, move_cursor=False)
            
            if is_pressed('right'):
                self.right()
            elif is_pressed('left'):
                self.left()
            elif is_pressed('up'):
                self.up()
            elif is_pressed('down'):
                self.down()

selection_menu = SelectionMenu((12, 15), [Selection('1', (1, 1), (3, 3)), Selection('2', (1, 4), (3, 3)), Selection('3', (1, 7), (3, 3)), Selection('4', (1, 10), (3, 3))])
selection_menu.loop()

print(selection_menu.frame)