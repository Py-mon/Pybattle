from os import system
from time import sleep

from src.window.frame import Frame, Window

system('cls') # Change to "clear" if you are not on windows

main = Window((40, 60))
main.add_frame(Frame((6, 20)), (3, 3))
main.add_frame(Frame((2, 2)))

