from pybattle.creatures.humanoid import Humanoid
from pybattle.creatures.pymon import Pymon

#      /\_/\
#    ( o   o )
#   ==( I^I )==
#      /   \

#    /_/\
#   ( o o )
# ==( I^I )==
#     / \


#  (_/)
# (='.'=)
#  (")(")


#  /\_/\
# ( o.o )
#  > ^ <

#    (\(\
#  =( 0 0 )=
#   (")_(")


class Sciture(Pymon):
    """A swift squirrel. Comes from the Latin word sciurus.

    Sci-ture."""

    bases = {
        "attack": 80,  ##
        "energy": 120,  ######
        "defense": 90,  ###
        "magic": 70,  #
        "speed": 130,  #######
        "health": 110,  #####
    }


class Cobolor(Humanoid):
    """A fierce goblin. Comes from the Latin word cobolorum.

    Co-bo-lor
    """

    # Total: 600
    bases = {
        "attack": 120,  ######
        "energy": 80,  ##
        "defense": 110,  #####
        "magic": 120,  ######
        "speed": 70,  #
        "health": 100,  ####
    }


class Vexifurr(Pymon):
    # Health: 122
    # Speed: 76
    # Physical Attack: 92
    # Physical Defense: 110
    # Toxin/Venom/Disease Defense: 95
    # Toxin/Venom Damage: 105
    # Total: 600

    bases = {
        "attack": 80,  ##
        "energy": 120,  ######
        "defense": 90,  ###
        "magic": 70,  #
        "speed": 76,  #######
        "health": 122,  #####
    }
