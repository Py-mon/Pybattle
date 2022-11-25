from os import system
from time import sleep

from src.window.frame import Frame, Window

system('cls')

main = Window((40, 20))
main.add_frame(Frame((20, 10)))
# main.add_frame(Frame((12, 3)))
sleep(5)
