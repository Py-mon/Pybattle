from .humanoid import Humanoid
from .pymon import Pymon


class Sciture(Pymon):
    """A swift squirrel. Comes from the Latin word sciurus.

    Sci-ture"""
    # Total: 600
    bases = {
        'attack':  80,
        'energy':  120,
        'defense': 90,
        'magic':   70,
        'speed':   130,
        'health':  110,
    }


class Cobolor(Humanoid):
    """A fierce goblin. Comes from the Latin word cobolorum.

    Co-bol-or
    """
    # Total: 600
    bases = {
        'attack':  120,
        'energy':  80,
        'defense': 110,
        'magic':   120,
        'speed':   70,
        'health':  100,
    }
