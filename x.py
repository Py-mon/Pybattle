# from pybattle import alignment
# from pybattle.battle import battle
# from pybattle.creatures.attributes import ability
# from pybattle.creatures.attributes import element
# from pybattle.creatures.attributes import item
# from pybattle.creatures.attributes import move
# from pybattle.creatures.attributes import reinforcements
# from pybattle.creatures.attributes import status_ailment
# from pybattle.creatures.attributes import trait
# from pybattle.creatures.graphics import animal_graphics
# from pybattle.creatures.graphics import graphics
# from pybattle.creatures import humanoid
# from pybattle.creatures import pymon
# from pybattle.creatures import rand
# from pybattle.creatures import species
# from pybattle.log import errors
# from pybattle.log import log
# from pybattle.screen import colors
# from pybattle.screen.frames.border import border_type
# from pybattle.screen.frames.border import junction_table
# from pybattle.screen.frames import frame
# from pybattle.screen.frames import map
# from pybattle.screen.frames import menu
# from pybattle.screen.frames import weather
# from pybattle.screen.grid import cell
# from pybattle.screen.grid import matrix
# from pybattle.screen.grid import nested
# from pybattle.screen.grid import point
# from pybattle.screen import sound
# from pybattle.screen import window
# from pybattle import types_

# packages = []
# for key, value in globals().copy().items():
#     path = str(value)[str(value).find("from") + 6 : -2]

#     with open(path) as f:
#         file = str(f.read())
#         file.


#     if "_" not in key:
#         packages.append(key)
import string
import random

def generate_random_password():
	possible_chars = list(string.ascii_letters + string.digits + "!@#$%^&*")
	password_length = 10 
	password = []
	for i in range(password_length):
		password.append(random.choice(possible_chars))

	random.shuffle(password)

	return ('Random password: '+''.join(password))



