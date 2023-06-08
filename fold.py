import time

import keyboard

keyboard.press_and_release("ctrl+p")
keyboard.write("time.log")
time.sleep(0.1)
keyboard.press_and_release("enter")
keyboard.press_and_release('ctrl+k+0')
