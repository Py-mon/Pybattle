from src.creatures.species import Sciture
from src.creatures.species import Cobolor
from src.creatures.attributes.reinforcements import Armor
from src.creatures.humanoid import Humanoid

s = Sciture()
c = Cobolor()
a = Armor(1.5, 10)
h = Humanoid()
print(s.bases)
print(c.bases)
print(a)
print(h)