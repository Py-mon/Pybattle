from os import system
from time import sleep

from src.window.frame import Frame, Window

system('cls')

main = Window((40, 60))
main.add_frame(Frame((6, 20)), (3, 3))
main.add_frame(Frame((2, 2)))

