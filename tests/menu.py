# mfrom pybattle.window.menus.list_menu import ListMenu
from pybattle.screen.grid.size import Size
from pybattle.screen.grid.coord import Coord
from screen.frames.frame import Frame


menu = ListMenu(Frame(Size(10, 20)), ['Play', 'Settings', 'Quit'])

print(menu._event())
