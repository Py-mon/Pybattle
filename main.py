from os import system
from time import sleep

from source.window.frame import Frame, Window

system('cls')

main = Window((24, 12))
main.add_frame(Frame((12, 5)))
# main.add_frame(Frame((12, 3)))
sleep(5)