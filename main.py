from src.creatures.species import Sciture
from src.creatures.species import Cobolor
from src.creatures.attributes.reinforcements import Armor
from src.creatures.humanoid import Humanoid
from src.window.frame import MainFrame, Frame

# s = Sciture()
# c = Cobolor()
# a = Armor(1.5, 10)
# h = Humanoid()
# print(s.bases)
# print(c.bases)
# print(a)
# print(h)


x = MainFrame(40, 20)
x.add_frame(Frame(3, 3), 0, 0)
x.add_frame(Frame(3, 3), 1, 1)
x.add_frame(Frame(3, 3), 4, 1)
x.add_frame(Frame(3, 3), 7, 1)

x.add_frame(Frame(10, 10), 15, 10)
x.add_frame(Frame(5, 5), 15, 1)
x.add_frame(Frame(2, 8), 7, 8)

x.add_frame(Frame(3, 9), 1, 7)
x.add_frame(Frame(10, 10), 30, 1)
x.add_frame(Frame(4, 4), 7, 4)
# print(Frame((3, 24)).frame)
# for i in range(1, 20):
# 	for j in range(1, 5):
# 		x.add_frame(Frame(3, 3), 3 * i, 3 * j)
# x.add_frame(Frame(10, 6), 8, 1)
# x.add_frame(Frame(5, 5), 0, 0)
# x.add_frame(Frame(4, 4), 2, 6)