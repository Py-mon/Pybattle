from pybattle.creatures.pymon import Pymon
from pybattle.types_ import Creature
from pybattle.screen.grid.matrix import Matrix
from pybattle.screen.grid.cell import Cell
from pybattle.screen.grid.point import Coord, Size
from pybattle.screen.frames.frame import Frame
from pybattle.screen.frames.menu import (
    Menu,
    Selection,
    SwitchSelection,
    VoidSelection,
    FrameSelection,
)


class Battle:
    def __init__(self, attacker: Creature, defender: Creature) -> None:
        self.attacker = attacker
        self.defender = defender

    def menu(self):
        m = Menu(
            Cell.from_size(Size(5, 30)),
            [
                SwitchSelection(
                    FrameSelection(Frame.centered("Punch", Size(3, 7)), Coord(1, 7)),
                    FrameSelection(Frame.centered("Punch", Size(3, 7)), Coord(1, 7)),
                ),
                SwitchSelection(
                    FrameSelection(Frame.centered("Slash", Size(3, 7)), Coord(1, 7)),
                    FrameSelection(Frame.centered("Slash", Size(3, 7)), Coord(1, 7)),
                ),
                SwitchSelection(
                    FrameSelection(Frame.centered("Dodge", Size(3, 7)), Coord(1, 7)),
                    FrameSelection(Frame.centered("Dodge", Size(3, 7)), Coord(1, 7)),
                ),
            ],
        )
        print(m)

        # move_titles = [move for move in enumerate(self.attacker.moves)]


m = Menu(
    Cell.from_size(Size(5, 30)),
    [
        SwitchSelection(
            FrameSelection(Frame.centered("Punch", Size(3, 7)), Coord(1, 1)),
            FrameSelection(Frame.centered("Punch", Size(3, 7)), Coord(1, 1)),
        ),
        SwitchSelection(
            FrameSelection(Frame.centered("Slash", Size(3, 7)), Coord(1, 9)),
            FrameSelection(Frame.centered("Slash", Size(3, 7)), Coord(1, 9)),
        ),
        SwitchSelection(
            FrameSelection(Frame.centered("Dodge", Size(3, 7)), Coord(1, 17)),
            FrameSelection(Frame.centered("Dodge", Size(3, 7)), Coord(1, 17)),
        ),
    ],
)
print(m)
"""
╭─────────────────────────────╮
│  ╭─Punch─┬───────┬───────╮  │
│  │       │       │       │  │
│  │ Punch │ Slash │ Dodge │  │
│  │ 50    │ 70    │       │  │
│  ╰───────┴───────┴───────╯  │
╰─────────────────────────────╯

╭─Punch──┬────────┬────────╮
│        │        │        │
│ Punch  │ Slash  │ Dodge  │
│ 50     │ 70     │        │
╰────────┴────────┴────────╯
── ⎯  —— –– ‒‒ ‑‑ ‐‐ _⎽⎼⎻⎺ ⎹ ⎸ ╲ ╱ ╷ ╶ ╵ ╴ ⏗ ⎾⎺⏋


     
╭─ Punch ─┬─ Slash ─┬─────────┬─────────╮
│ 50 STR  │         │         │         │
│ 26 EC   │ Slash   │ Slash   │ Dodge   │
│         │ 70      │ 70      │         │
╰─────────┴─────────┴─────────┴─────────╯


╭─ Punch ─┬─ Slash ─┬─────────┬─────────╮
│ 50 STR  │ Normal  │         │         │
│         │         │ Slash   │ Dodge   │
│         │ 26 EC   │         │ 70      │
╰─────────┴─────────┴─────────┴─────────╯
    
  ╭─ WIND BASH ─╮  
  │ Combative   ├─ Slash ─┬─ Dodge ─╮
  │   30 EC     │ Normal  │         │
  │  50 STR     │ 26 EC   │ 26 EC   │
  │  100% ACC   ├─────────┴─────────╯
  ╰──────── AIR ╯
  
  
  
  ╭─ WIND BASH ─╮  
  │ Combative   ├─ Slash ─┬─ Dodge ─╮
  │   30 EC     │ Normal  │         │
  │  50 STR     │ 26 EC   │ 26 EC   │
  │  100% ACC   ├─────────┴─────────╯
  ╰──────── AIR ╯



A1 
╭─────────────────────────────────────────────╮
│ ╭─ Wind Bash ─ Air ─╮ ╭─ Slash ── Normal ─╮ │
│ │ 50 STR    90% ACC │ │ 35 STR   100% ACC │ │
│ │ Physical    25 EC │ │ Physical    20 EC │ │
│ ╰───────────────────╯ ╰───────────────────╯ │
│ ╭─ Dodge ───────────╮ ╭─ Tornado ─── Air ─╮ │
│ │           80% ACC │ │ 70 STR    95% ACC │ │
│ │ Support     30 EC │ │ Magical     50 EC │ │
│ ╰───────────────────╯ ╰───────────────────╯ │
╰─────────────────────────────────────────────╯

A2 (Side Connected)

╭─ Wind Bash ─ Air ─┬─ Slash ── Normal ─╮
│ 50 STR    90% ACC │ 35 STR   100% ACC │
│ Physical    25 EC │ Physical    20 EC │
╰───────────────────┴───────────────────╯
╭─ Dodge ───────────┬─ Tornado ─── Air ─╮
│           80% ACC │ 70 STR    95% ACC │
│ Support     30 EC │ Magical     50 EC │
╰───────────────────┴───────────────────╯
 
A3 (All Connected)

╭─ Wind Bash ─ Air ─┬─ Slash ── Normal ─╮
│ 50 STR    90% ACC │ 35 STR   100% ACC │
│ Physical    25 EC │ Physical    20 EC │
├───────────────────┴───────────────────┤
├─ Dodge ───────────┬─ Tornado ─── Air ─┤
│           80% ACC │ 70 STR    95% ACC │
│ Support     30 EC │ Magical     50 EC │
╰───────────────────┴───────────────────╯

A4 (Any Size)
╭────────────────────────────────────────────╮
│ ╭─ Wind Bash ─ Air ─╮ ╭─ Slash ─ Normal ─╮ │
│ │ 50 STR    90% ACC │ │ 35 STR  100% ACC │ │
│ │ Physical    25 EC │ │ Physical   20 EC │ │
│ ╰───────────────────╯ ╰──────────────────╯ │
│    ╭─ Dodge ────────╮ ╭─ Tornado ─ Air ─╮  │
│    │        80% ACC │ │ 70 STR  95% ACC │  |
│    │ Support  30 EC │ │ Magical   50 EC │  |
│    ╰────────────────╯ ╰─────────────────╯  │
╰────────────────────────────────────────────╯


B1 (Simple)

╭─ Wind Bash ─ Air ─╮ ╭─ Slash ── Normal ─╮
│ 50 STR      25 EC │ │ 35 STR      20 EC │
╰───────────────────╯ ╰───────────────────╯
╭─ Dodge ───────────╮ ╭─ Tornado ─── Air ─╮
│ Support     30 EC │ │ 70 STR      50 EC │
╰───────────────────╯ ╰───────────────────╯


B2 (Bottom Extends)

╭─ Wind Bash ─ Air ─╮ ╭─ Slash ── Normal ─╮
│ 50 STR    90% ACC │ │ 35 STR      20 EC │
│ Physical    25 EC │ ╰───────────────────╯
╰───────────────────╯ 
╭─ Dodge ───────────╮ ╭─ Tornado ─── Air ─╮
│ Support     30 EC │ │ 70 STR      50 EC │
╰───────────────────╯ ╰───────────────────╯


B3 (Top Extends)

╭─ Wind Bash ─ Air ─╮ ╭─ Slash ── Normal ─╮
│ 50 STR    90% ACC │ │ 35 STR      20 EC │
╰───────────────────╯ ╰ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╯
                      ╭─ Tornado ─── Air ─╮
╭─ Dodge ───────────╮ │ 70 STR    95% ACC │
│ Support     30 EC │ │ Magical     50 EC │
╰───────────────────╯ ╰───────────────────╯



B3 (Corner Extends)


  ╭─ Wind Bash ─ Air ─╮ ╭─ Slash ── Normal ─╮
  │ 50 STR      25 EC │ │ 35 STR      20 EC │
  ╰───────────────────╯ ╰───────────────────╯
  ╭─ Dodge ── Normal ─╮ ╭─ Tornado ───── Air ─╮
  │ Support     30 EC │ │ 70 STR      95% ACC │
  ╰───────────────────╯ │ Magical       50 EC │
                        ╰─────────────────────╯


C1  
╭─ Wind Bash ─╮  
│ 50 STR      │─ Slash ──┬╴Dodge╶─╮
│       35 EC │   25 EC  │  30 EC │
│ 100% ACC    │─ Normal ─┴╴Normal╶╯
╰──────── Air ╯

C2  
           ╭─ Slash ────╮  
╭─ Slash ──│ • 30 STR   │─ Dodge ──╮
│ • 25 EC  │ • 25 EC    │ • 30 EC  │
╰─ Normal ─│ • 100% ACC │─ Normal ─╯
           ╰─────── Air ╯





─	━	│	┃	┄	┅	┆	┇	┈	┉	┊	┋	┌	┍	┎	┏

U+251x	┐	┑	┒	┓	└	┕	┖	┗	┘	┙	┚	┛	├	┝	┞	┟

U+252x	┠	┡	┢	┣	┤	┥	┦	┧	┨	┩	┪	┫	┬	┭	┮	┯

U+253x	┰	┱	┲	┳	┴	┵	┶	┷	┸	┹	┺	┻	┼	┽	┾	┿

U+254x	╀	╁	╂	╃	╄	╅	╆	╇	╈	╉	╊	╋	╌	╍	╎	╏

U+255x	═	║	╒	╓	╔	╕	╖	╗	╘	╙	╚	╛	╜	╝	╞	╟

U+256x	╠	╡	╢	╣	╤	╥	╦	╧	╨	╩	╪	╫	╬	╭	╮	╯

U+257x	╰	╱	╲	╳	╴	╵	╶	╷	╸	╹	╺	╻	╼	╽	╾	╿

"""
