# mfrom pybattle.window.menus.list_menu import ListMenu
from pybattle.window.grid.size import Size
from pybattle.window.grid.coord import Coord
from window.frames.frame import Frame


menu = ListMenu(Frame(Size(10, 20)), ['Play', 'Settings', 'Quit'])

print(menu._event())
