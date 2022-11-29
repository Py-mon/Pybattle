from src.window.frame import Frame
from src.window.coord import Coord
from src.types_ import CoordReference
from src.window.size import Size
from src.window.screen import Color


class SelectionMenu:
    def __init__(self, selections: dict[str, CoordReference], default_color: Color = Color.GRAY) -> None:
        for coord in selections:
            selections[coord] = Coord.convert_reference(selections[coord])
        self.selections = selections

        coords = list(self.selections.values())
        coords.sort(key=lambda coord: coord.x ** 2 + coord.y ** 2)
        farthest_coord = coords[-1]

        width = max([Frame(selection).width for selection in self.selections.keys()])
        height = max([Frame(selection).height for selection in self.selections.keys()])

        size = Size(farthest_coord.x + 1 + width, farthest_coord.y + 1 + height)

        self.selection = list(selections.keys())[0]

        self.frame = Frame(size=size)
        for selection, location in self.selections.items():
            if selection == self.selection:
                print(Frame(selection, default_color).matrix)
                self.frame.add_frame(Frame(selection, default_color), location)
            else:
                self.frame.add_frame(Frame(selection), location)


SelectionMenu({'a': (1, 1), 'b': (4, 4), 'c': (9, 9)})


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