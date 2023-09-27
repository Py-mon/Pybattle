from pybattle.screen.grid.matrix import Grid


y = "╱____╲_____╱╱   ── ⎯  —— –– ‒‒ ‑‑ ‐‐ _⎽⎼⎻⎺ ⎹ ⎸ ╲ ╱ ╷ ╶ ╵ ╴ ⏗ ⎾⎺⏋"
print(y)
#                                                           ⎿⎽⏌

# ╭─ BEDROOM ─┬──────────────────╮
# │   ╰───────╯       ||||       │
# │                   ||||       │
# │                     ─┬─┬─┬─┬─┤
# │                              │
# │                              │
# │╭│╮   ╶─╮                     │
# ││││    ░│                     │
# │╰│╯   ╶─╯           ╭─────┬─╮ │
# │                    │░░░░░│▓│ │
# │                    ╰─────┴─╯ │
# ╰──────────────────────────────╯

from copy import copy
from os import system
from random import randint, random
from textwrap import dedent
from time import sleep
from typing import Optional

from pybattle.screen.colors import Color, Colors
from pybattle.screen.frames.frame import Frame
from pybattle.screen.frames.map import Map
from pybattle.screen.frames.menu import Menu, Selection, SwitchSelection, VoidSelection
from pybattle.screen.frames.weather import Rain, Weather
from pybattle.screen.grid.matrix import Cell
from pybattle.screen.grid.point import Coord, Size
from pybattle.screen.window import Event, EventExit, EventQueue, Window, keys_pressing
from pybattle.types_ import CardinalDirection


def read_graphic_file(file):
    with open(file, encoding="utf-8") as f:
        text = f.read()
        matrix = Grid(Cell.from_str(text[: text.find("%")]))
        return matrix


DEFAULT_CHARACTER = read_graphic_file(
    r"pybattle\creatures\graphics\default_character.g"
)
DEFAULT_BODY = read_graphic_file(r"pybattle\creatures\graphics\default_body.g")

# print(DEFAULT_CHARACTER)

# class Animation:
#     def __init__(self, for_, frames, speed, repeats: bool = False):
#         self.frames = frames
#         self.speed = speed
#         self.repeats = repeats
#         self.frame = 0

#         def update(obj):
#             obj.cells = frames[self.frame].cells
#             self.frame += 1

#         self.event = Event(update, speed, for_)


class Face:
    BLINK_CHANCE = 0.03

    def __init__(
        self, eyes: Cell, mouth: Cell, blink: bool = True, blink_cell: Cell = ...
    ):
        self.eyes = eyes
        self.mouth = mouth
        self.blink = blink
        self.blink_cell = blink_cell

    @property
    def straight_on(self) -> tuple[tuple[Cell, ...], ...]:
        face = Grid(
            Cell.from_str(
                dedent(
                    """\
            │     │
            │     │
            """
                )
            )
        )

        face[Coord(1, 3)] = self.mouth

        if self.blink and random() < type(self).BLINK_CHANCE:
            if self.blink_cell is ...:
                self.blink_cell = Cell("_", self.eyes.color)

            face[Coord(0, 2)] = self.blink_cell
            face[Coord(0, 4)] = self.blink_cell

        else:
            face[Coord(0, 2)] = self.eyes
            face[Coord(0, 4)] = self.eyes

        return face.cells

    @property
    def look_left(self):
        if self.blink and random() < type(self).BLINK_CHANCE:
            face = f"""\
            │_ _  │
            │ {self.mouth}   │
            """
        else:
            face = f"""\
            │{self.eyes} {self.eyes}  │
            │ {self.mouth}   │
            """

        return Cell.from_str(dedent(face))

    @property
    def look_right(self):
        if self.blink and random() < type(self).BLINK_CHANCE:
            face = f"""\
            │  _ _│
            │   {self.mouth} │
            """
        else:
            face = f"""\
            │  {self.eyes} {self.eyes}│
            │   {self.mouth} │
            """

        return Cell.from_str(dedent(face))


class MaleHair:
    def __init__(
        self,
        straight_on: tuple[Cell, ...],
        left: Optional[tuple[Cell, ...]] = None,
        right: Optional[tuple[Cell, ...]] = None,
    ):
        self.straight_on = straight_on

        self.left = left or self.straight_on
        self.right = right or self.straight_on


class HelmetGraphics:
    def __init__(
        self,
        straight_on: Grid,
        left: Optional[Grid] = None,
        right: Optional[Grid] = None,
        icon: Optional[Grid] = None,
    ):
        self.straight_on = straight_on

        self.left = left or self.straight_on
        self.right = right or self.straight_on

        self.icon = icon


class Head:
    def __init__(self, hair: MaleHair, face: Face):
        self.hair = hair
        self.face = face


class WeaponGraphics:
    def __init__(
        self,
        right: Grid,
        left: Grid,
        attack_left: Optional[list[Grid]] = None,  # use in battle
        attack_right: Optional[list[Grid]] = None,
        image: Optional[str] = None,
        icon: Optional[str] = None,
    ):
        # self.left = left
        self.right = right

        if attack_left:
            self.attack_left = attack_left
        if attack_right:
            self.attack_right = attack_right

        self.image = image
        self.icon = icon


class ItemGraphics:
    def __init__(self, graphics: Grid):
        # "`x`'s will be ignored"
        self.graphics = graphics


class Body:
    def __init__(
        self,
        body: Grid,
        icon: Optional[str] = None,
    ):
        self.body = body
        self.body.extend_column(Cell.from_size(Size(1, self.body.size.height))[0], -1)
        self.body.remove_whitespace_sides()

        self.icon = icon


class Character:
    def __init__(
        self,
        body: Body = Body(DEFAULT_BODY),
        head: Optional[HelmetGraphics | Head] = None,
        weapon_graphics: Optional[WeaponGraphics] = None,
        item_graphics: Optional[ItemGraphics] = None,
        icon: Optional[str] = None,
    ):
        """9x13
        ```
          _-----_
          │ , , │
          │  -  │
         _─╵───╵─_
        ╱ │     │ ╲
        ╲ │_____│ ╱
         ^│ ╭─╮ │^
          │ │ │ │
          │_│ │_│
        """
        self.body = body
        self.head = head
        self.weapon = weapon_graphics
        self.icon = icon
        self.item_graphics = item_graphics

        self.spaces = Cell.from_size(Size(1, 3))[0]

    def apply_head_position(self, character, face_rows, hair_row):
        for line in reversed(face_rows):
            character.extend_row(self.spaces + line, -1)
        character.extend_row(self.spaces + hair_row, -1)

    def item(self, character):
        if not self.item_graphics:
            return

        for coord, cell in self.item_graphics.graphics.dct.items():
            if cell.value == " ":
                continue
            character[coord] = cell

    @property
    def straight_on(self):
        character = copy(self.body.body)
        if isinstance(self.head, Head):
            self.apply_head_position(
                character,
                self.head.face.straight_on,
                self.head.hair.straight_on,
            )
        elif isinstance(self.head, HelmetGraphics):
            character.overlay(self.head.straight_on, Coord(0, 2))

        if self.weapon:
            character.overlay(self.weapon.right, Coord(0, 10))

        self.item(character)

        return str(character)

    @property
    def left(self):
        character = copy(self.body.body)
        if isinstance(self.head, Head):
            self.apply_head_position(
                character,
                self.head.face.look_left,
                self.head.hair.left,
            )
        elif isinstance(self.head, HelmetGraphics):
            character.overlay(self.head.left, Coord(0, 2))

        if self.weapon:
            character.overlay(self.weapon.right, Coord(0, 10))

        self.item(character)

        return str(character)

    @property
    def right(self):
        character = copy(self.body.body)
        if isinstance(self.head, Head):
            self.apply_head_position(
                character,
                self.head.face.look_right,
                self.head.hair.right,
            )
        elif isinstance(self.head, HelmetGraphics):
            character.overlay(self.head.right, Coord(0, 3))

        if self.weapon:
            character.overlay(self.weapon.right, Coord(0, 10))

        self.item(character)

        return str(character)


x = Character(
    head=Head(MaleHair(Cell.from_str("_-/|\\-_")[0]), Face(Cell(","), Cell("-"))),
    weapon_graphics=WeaponGraphics(
        Grid(
            Cell.from_str(
                """\




_ ^
 ╲│
  ^
  │
  │
  │"""
            )
        ),
        None,
    ),
    # item_graphics=ItemGraphics(
    #     Matrix(
    #         Cell.from_str(
    #             """\
    #  ╲ ╱
    # __̲*__│ .^
    #           """
    #         )
    #     )
    # ),
)
print(x.straight_on)


# ╭─ BEDROOM ─┬──────────────────╮
# │   ╰───────╯       ||||       │
# │                   ||||       │
# │                     ─┬─┬─┬─┬─┤
# │                              │
# │                              │
# │╭│╮   ╶─╮                     │
# ││││    ░│                     │
# │╰│╯   ╶─╯           ╭─────┬─╮ │
# │                    │░░░░░│▓│ │
# │                    ╰─────┴─╯ │
# ╰──────────────────────────────╯

x = Grid(
    Cell.from_str(
        """
  _-----_      
  │ , , │      
  │  -  │      
 _─╵---╵─_     
╱ │     │ ╲    
╲ │_____│ ╱    
 ^│ ╭─╮ │^     
  │ │ │ │      
  │_│ │_│      
"""
        """ 
  _-----_      
  │  , ,│      
  │   ` │      
 _─╵---╵─__
╱ │     │  ╲    
╲ │_____│  ╱     
 ^╱ ⸝─⸜ ╲ ^     
 ╱ ╱   ╲ ╲      
 │_│    │_│   
"""
    )
)
"""
  _-----_      
  │ , , │      
  │  ᵕ  │      
 _─╵---╵─_     
╱ │     │ ╲    
╲ │_____│ ╱    
 ^│ ╭─╮ │^    
  │_│ │_│      
"""
# ⁕⁔⠄⸜⸝
"""
  _-----_      
  │ , , │      
  │  `  │      
 _─╵---╵─_     
╱ │     │ ╲    
╲ │_____│ ╱    
 ^│ ╭─╮ │^    
  │_│ │_│      
"""
"""# ʻʼʽ،⸲
  _-----_      
  │ . . │      
  │  ~  │      
 _─╵---╵─_     
╱ │     │ ╲    
╲ │_____│ ╱    
 ^│ ╭─╮ │^    
  │ │ │ │     
  │_│ │_│      
"""
"""# ʻʼʽ،⸲
  _-----_      
  │, ,  │      
  │ -   │      
 _─╵---╵─_     
╱ │     │ ╲    
╲ │_____│ ╱    
 ^│ ╭─╮ │^    
  │ │ │ │     
  │_│ │_│      
"""

x = """
   _╷╷╷╷╷_
  ╱│ , , │╲
 * │  ᵕ  │ *
  _─╵---╵─_
 ╱ ╲ . . ╱ ╲
^  ╱. . .╲ ^
  ╱_______╲
   ╱_│ │_╲
"""


# wg = WeaponGraphics(
#     Animation(
#         """\


#  ^
# ╲│
#  ^
#  │
#  │
#  │
# """,
#         1,
#     ),
#     Animation(None, None),
#     "",
#     "",
# )

# f = Frame(Cell.from_size(Size(12, 30)))
# y = Matrix(Cell.from_str(wg.idle.frames))
# print(y)
# x.overlay(y, Coord(0, 10))
# print(repr(x))
# f.overlay(x, Coord(1, 5))

# w = Window(f)
# w.run()


# x = Matrix(Cell.from_str("""
#    _-----_
#    | , , |
#    |  -  |
#   __|---|__
#  / |     | \
#  \ |_____| /
#   ^| | | |^
#    | | | |
#    |_| |_|

# """))
# ╭─ BEDROOM ─┬──────────────────╮
# │   ╰───────╯       ||||       │
# │                   ||||       │
# │                     ─┬─┬─┬─┬─┤
# │                              │
# │                              │
# │╭│╮   ╶─╮                     │
# ││││    ░│                     │
# │╰│╯   ╶─╯           ╭─────┬─╮ │
# │                    │░░░░░│▓│ │
# │                    ╰─────┴─╯ │
# ╰──────────────────────────────╯
x = """
   _-----_
   │ , , │
   │  -  │
  _─╵---╵─_ ^
 ╱ │     │ ╲│
 ╲ │_____│  ^
  ^│ ╭─╮ │  │
   │ │ │ │  │
   │_│ │_│  │
"""
x = """
   _-----_   
   │ , , │   
   │  -  │ 
  _─╵---╵─_  
 ╱ │     │ ╲ 
 ╲ │_____│ ╱ 
  ^│ ╭─╮ │^ 
   │ │ │ │  
   │_│ │_│   
"""

x = """
   _-----_   
   │ , , │   
   │  -  │ 
  _─╵---╵─_  
 ╱ │     │ ╲ 
 ╲ │_____│ ╱ 
  ^│ ╭─╮ │^ 
   │ │ │ │  
   │_│ │_│   
"""

# ╷ ╶ ╵ ╴
x = """
   _-----_   
   │ , , │   
   │  -  │ 
  _─╵---╵─__     
 ╱ │     │  ⎺⎺<─┼────
 ╲ │_____│      
  ^│ ╭─╮ │ 
   │ │ │ │  
   │_│ │_│   
"""

x = """
   _╷╷╷╷╷_
  ╱│ , , │╲
 * │  -  │ *
  _─╵---╵─_
 ╱ ╲ . . ╱ ╲
 ^ ╱. . .╲  ^
  ╱_______╲
   ╱_│ │_╲
"""


x = r"""
   _-----_
   │ , , │
   │  -  │
  _─╵---╵─_  ^
 ╱ │     │ ╲ │
 ╲ │_____│  <│
  ^│ ╭─╮ │   │
   │ │ │ │   │
   │_│ │_│   │
"""

x = r"""
   _-----_
   │ , , │
   │  -  │
  _─╵---╵─_  ^
 ╱ ╲     ╱ ╲ │
 ╲ ╱_____╲  ^│
  ^│ ╭─╮ │   │
   │ │ │ │   │
   │_│ │_│   │
"""
x = """
   _╷╷╷╷╷_
  ╱│ , , │╲
 * │  -  │ *
  _─╵---╵─_
 ╱ ╲ . . ╱ ╲
 ^ ╱. . .╲  ^
  ╱_______╲
   ╱_│ │_╲
"""

x = """
   _-----_
   │ , , │
   │  -  │   ╷
  _─╵---╵─_  │
 ╱ │     │ ╲ ┼
 ╲ │_____│  <│
  ^│ ╭─╮ │
   │ │ │ │
   │_│ │_│
"""
x = """
   _-----_
   │ , , │
   │  -  │   ╷
  _─╵---╵─_  │
 ╱ ╷     ╷ ╲ ┼
 ╲ │_____│  <╵
  ˄│ ╭─╮ │
   │_│ │_│
"""
# x = '╱____╲_____╱╱   ── ⎯  —— –– ‒‒ ‑‑ ‐‐ _⎽⎼─⎻⎺ ⎹ ⎸ ╲ ╱ ╷ ╶ ╵ ╴ ⏗ ⌠⎾⎺⏋'
# ┐┌└ ┘
# w = Window(Matrix(Cell.from_str(x)))
# w.run()

# ⤉￪
#  "Modifier Letter Left Arrowhead (no. 706 U+02C2)": "˂",
#  "Modifier Letter Right Arrowhead (no. 707 U+02C3)": "˃",
#  "Modifier Letter Up Arrowhead (no. 708 U+02C4)": "˄",
#  "Modifier Letter Down Arrowhead (no. 709 U+02C5)": "˅",

# Egypt
# 𓀂 𓀝
#  |  |
# 𓀟x 𓏼x
x = """
# 𓀀	𓀁	𓀂	𓀃	𓀄	𓀅	𓀆	𓀇	𓀈	𓀉	𓀊	𓀋	𓀌	𓀍	𓀎	𓀏
# U+1301x	𓀐	𓀑	𓀒	𓀓	𓀔	𓀕	𓀖	𓀗	𓀘	𓀙	𓀚	𓀛	𓀜	𓀝	𓀞	𓀟
# U+1302x	𓀠	𓀡	𓀢	𓀣	𓀤	𓀥	𓀦	𓀧	𓀨	𓀩	𓀪	𓀫	𓀬	𓀭	𓀮	𓀯
# U+1303x	𓀰	𓀱	𓀲	𓀳	𓀴	𓀵	𓀶	𓀷	𓀸	𓀹	𓀺	𓀻	𓀼	𓀽	𓀾	𓀿
# U+1304x	𓁀	𓁁	𓁂	𓁃	𓁄	𓁅	𓁆	𓁇	𓁈	𓁉	𓁊	𓁋	𓁌	𓁍	𓁎	𓁏
# U+1305x	𓁐	𓁑	𓁒	𓁓	𓁔	𓁕	𓁖	𓁗	𓁘	𓁙	𓁚	𓁛	𓁜	𓁝	𓁞	𓁟
# U+1306x	𓁠	𓁡	𓁢	𓁣	𓁤	𓁥	𓁦	𓁧	𓁨	𓁩	𓁪	𓁫	𓁬	𓁭	𓁮	𓁯
# U+1307x	𓁰	𓁱	𓁲	𓁳	𓁴	𓁵	𓁶	𓁷	𓁸	𓁹	𓁺	𓁻	𓁼	𓁽	𓁾	𓁿
# U+1308x	𓂀	𓂁	𓂂	𓂃	𓂄	𓂅	𓂆	𓂇	𓂈	𓂉	𓂊	𓂋	𓂌	𓂍	𓂎	𓂏
# U+1309x	𓂐	𓂑	𓂒	𓂓	𓂔	𓂕	𓂖	𓂗	𓂘	𓂙	𓂚	𓂛	𓂜	𓂝	𓂞	𓂟
# U+130Ax	𓂠	𓂡	𓂢	𓂣	𓂤	𓂥	𓂦	𓂧	𓂨	𓂩	𓂪	𓂫	𓂬	𓂭	𓂮	𓂯
# U+130Bx	𓂰	𓂱	𓂲	𓂳	𓂴	𓂵	𓂶	𓂷	𓂸	𓂹	𓂺	𓂻	𓂼	𓂽	𓂾	𓂿
# U+130Cx	𓃀	𓃁	𓃂	𓃃	𓃄	𓃅	𓃆	𓃇	𓃈	𓃉	𓃊	𓃋	𓃌	𓃍	𓃎	𓃏
# U+130Dx	𓃐	𓃑	𓃒	𓃓	𓃔	𓃕	𓃖	𓃗
#          |
# 𓃘	𓃙	𓃚x	𓃛	𓃜	𓃝	𓃞	𓃟
# U+130Ex	𓃠	𓃡	𓃢	𓃣	𓃤	𓃥	𓃦	𓃧	𓃨	𓃩	𓃪	𓃫	𓃬	𓃭	𓃮	𓃯
# U+130Fx	𓃰	𓃱	𓃲	𓃳	𓃴	𓃵	𓃶	𓃷	𓃸	𓃹	𓃺	𓃻	𓃼	𓃽	𓃾	𓃿
# U+1310x	𓄀	𓄁	𓄂	𓄃	𓄄	𓄅	𓄆	𓄇	𓄈	𓄉	𓄊	𓄋	𓄌	𓄍	𓄎	𓄏
# U+1311x	𓄐	𓄑	𓄒	𓄓	𓄔	𓄕	𓄖	𓄗	𓄘	𓄙	𓄚	𓄛	𓄜	𓄝	𓄞	𓄟
# U+1312x	𓄠	𓄡	𓄢	𓄣	𓄤	𓄥	𓄦	𓄧	𓄨	𓄩	𓄪	𓄫	𓄬	𓄭	𓄮	𓄯
# U+1313x	𓄰	𓄱	𓄲	𓄳	𓄴	𓄵	𓄶	𓄷	𓄸	𓄹	𓄺	𓄻	𓄼	𓄽	𓄾	𓄿
# U+1314x	𓅀	𓅁	𓅂	𓅃	𓅄	𓅅	𓅆	𓅇	𓅈	𓅉	𓅊	𓅋	𓅌	𓅍	𓅎	𓅏
# U+1315x	𓅐	𓅑	𓅒	𓅓	𓅔	𓅕	𓅖	𓅗	𓅘	𓅙	𓅚	𓅛	𓅜	𓅝	𓅞	𓅟
# U+1316x	𓅠	𓅡	𓅢	𓅣	𓅤	𓅥	𓅦	𓅧	𓅨	𓅩	𓅪	𓅫	𓅬	𓅭	𓅮	𓅯
# U+1317x	𓅰	𓅱	𓅲	𓅳	𓅴	𓅵	𓅶	𓅷	𓅸	𓅹	𓅺	𓅻	𓅼	𓅽	𓅾	𓅿
# U+1318x	𓆀	𓆁	𓆂	𓆃	𓆄	𓆅	𓆆	𓆇	𓆈	𓆉	𓆊	𓆋	𓆌	𓆍	𓆎	𓆏
# U+1319x	𓆐	𓆑	𓆒	𓆓	𓆔	𓆕	𓆖	𓆗	𓆘	𓆙	𓆚	𓆛	𓆜	𓆝	𓆞	𓆟
# U+131Ax	𓆠	𓆡	𓆢	𓆣	𓆤	𓆥	𓆦	𓆧	𓆨	𓆩	𓆪	𓆫	𓆬	𓆭	𓆮	𓆯
# U+131Bx	𓆰	𓆱	𓆲	𓆳	𓆴	𓆵	𓆶	𓆷	𓆸	𓆹	𓆺	𓆻	𓆼	𓆽	𓆾	𓆿
# U+131Cx	𓇀	𓇁	𓇂	𓇃	𓇄	𓇅	𓇆	𓇇	𓇈	𓇉	𓇊	𓇋	𓇌	𓇍	𓇎	𓇏
# U+131Dx	𓇐	𓇑	𓇒	𓇓	𓇔	𓇕	𓇖	𓇗	𓇘	𓇙	𓇚	𓇛	𓇜	𓇝	𓇞	𓇟
# U+131Ex	𓇠	𓇡	𓇢	𓇣	𓇤	𓇥	𓇦	𓇧	𓇨	𓇩	𓇪	𓇫	𓇬	𓇭	𓇮	𓇯
# U+131Fx	𓇰	𓇱	𓇲	𓇳	𓇴	𓇵	𓇶	𓇷	𓇸	𓇹	𓇺	𓇻	𓇼	𓇽	𓇾	𓇿
# U+1320x	𓈀	𓈁	𓈂	𓈃	𓈄	𓈅	𓈆	𓈇	𓈈	𓈉	𓈊	𓈋	𓈌	𓈍	𓈎	𓈏
# U+1321x	𓈐	𓈑	𓈒	𓈓	𓈔	𓈕	𓈖	𓈗	𓈘	𓈙	𓈚	𓈛	𓈜	𓈝	𓈞	𓈟
# U+1322x	𓈠	𓈡	𓈢	𓈣	𓈤	𓈥	𓈦	𓈧	𓈨	𓈩	𓈪	𓈫	𓈬	𓈭	𓈮	𓈯
# U+1323x	𓈰	𓈱	𓈲	𓈳	𓈴	𓈵	𓈶	𓈷	𓈸	𓈹	𓈺	𓈻	𓈼	𓈽	𓈾	𓈿
# U+1324x	𓉀	𓉁	𓉂	𓉃	𓉄	𓉅	𓉆	𓉇	𓉈	𓉉	𓉊	𓉋	𓉌	𓉍	𓉎	𓉏
# U+1325x	𓉐	𓉑	𓉒	𓉓	𓉔	𓉕	𓉖	𓉗	𓉘	𓉙	𓉚	𓉛	𓉜	𓉝	𓉞	𓉟
# U+1326x	𓉠	𓉡	𓉢	𓉣	𓉤	𓉥	𓉦	𓉧	𓉨	𓉩	𓉪	𓉫	𓉬	𓉭	𓉮	𓉯
# U+1327x	𓉰	𓉱	𓉲	𓉳	𓉴	𓉵	𓉶	𓉷	𓉸	𓉹	𓉺	𓉻	𓉼	𓉽	𓉾	𓉿
# U+1328x	𓊀	𓊁	𓊂	𓊃	𓊄	𓊅	𓊆	𓊇	𓊈	𓊉	𓊊	𓊋	𓊌	𓊍	𓊎	𓊏
# U+1329x	𓊐	𓊑	𓊒	𓊓	𓊔	𓊕	𓊖	𓊗	𓊘	𓊙	𓊚	𓊛	𓊜	𓊝	𓊞	𓊟
# U+132Ax	𓊠	𓊡	𓊢	𓊣	𓊤	𓊥	𓊦	𓊧	𓊨	𓊩	𓊪	𓊫	𓊬	𓊭	𓊮	𓊯
# U+132Bx	𓊰	𓊱	𓊲	𓊳	𓊴	𓊵	𓊶	𓊷	𓊸	𓊹	𓊺	𓊻	𓊼	𓊽	𓊾	𓊿
# U+132Cx	𓋀	𓋁	𓋂	𓋃	𓋄	𓋅	𓋆	𓋇	𓋈	𓋉	𓋊	𓋋	𓋌	𓋍	𓋎	𓋏
# U+132Dx	𓋐	𓋑	𓋒	𓋓	𓋔	𓋕	𓋖	𓋗	𓋘	𓋙	𓋚	𓋛	𓋜	𓋝	𓋞	𓋟
# U+132Ex	𓋠	𓋡	𓋢	𓋣	𓋤	𓋥	𓋦	𓋧	𓋨	𓋩	𓋪	𓋫	𓋬	𓋭	𓋮	𓋯
# U+132Fx	𓋰	𓋱	𓋲	𓋳	𓋴	𓋵	𓋶	𓋷	𓋸	𓋹	𓋺	𓋻	𓋼	𓋽	𓋾	𓋿
# U+1330x	𓌀	𓌁	𓌂	𓌃	𓌄	𓌅	𓌆	𓌇	𓌈	𓌉	𓌊	𓌋	𓌌	𓌍	𓌎	𓌏
# U+1331x	𓌐	𓌑	𓌒	𓌓	𓌔	𓌕	𓌖	𓌗	𓌘	𓌙	𓌚	𓌛	𓌜	𓌝	𓌞	𓌟
# U+1332x	𓌠	𓌡	𓌢	𓌣	𓌤	𓌥	𓌦	𓌧	𓌨	𓌩	𓌪	𓌫	𓌬	𓌭	𓌮	𓌯
# U+1333x	𓌰	𓌱	𓌲	𓌳	𓌴	𓌵	𓌶	𓌷	𓌸	𓌹	𓌺	𓌻	𓌼	𓌽	𓌾	𓌿
# U+1334x	𓍀	𓍁	𓍂	𓍃	𓍄	𓍅	𓍆	𓍇	𓍈	𓍉	𓍊	𓍋	𓍌	𓍍	𓍎	𓍏
# U+1335x	𓍐	𓍑	𓍒	𓍓	𓍔	𓍕	𓍖	𓍗	𓍘	𓍙	𓍚	𓍛	𓍜	𓍝	𓍞	𓍟
# U+1336x	𓍠	𓍡	𓍢	𓍣	𓍤	𓍥	𓍦	𓍧	𓍨	𓍩	𓍪	𓍫	𓍬	𓍭	𓍮	𓍯
# U+1337x	𓍰	𓍱	𓍲	𓍳	𓍴	𓍵	𓍶	𓍷	𓍸	𓍹	𓍺	𓍻	𓍼	𓍽	𓍾	𓍿
# U+1338x	𓎀	𓎁	𓎂	𓎃	𓎄	𓎅	𓎆	𓎇	𓎈	𓎉	𓎊	𓎋	𓎌	𓎍	𓎎	𓎏
# U+1339x	𓎐	𓎑	𓎒	𓎓	𓎔	𓎕	𓎖	𓎗	𓎘	𓎙	𓎚	𓎛	𓎜	𓎝	𓎞	𓎟
# U+133Ax	𓎠	𓎡	𓎢	𓎣	𓎤	𓎥	𓎦	𓎧	𓎨	𓎩	𓎪	𓎫	𓎬	𓎭	𓎮	𓎯
# U+133Bx	𓎰	𓎱	𓎲	𓎳	𓎴	𓎵	𓎶	𓎷	𓎸	𓎹	𓎺	𓎻	𓎼	𓎽	𓎾	𓎿
# U+133Cx	𓏀	𓏁	𓏂	𓏃	𓏄	𓏅	𓏆	𓏇	𓏈	𓏉	𓏊	𓏋	𓏌	𓏍	𓏎	𓏏
# U+133Dx	𓏐	𓏑	𓏒	𓏓	𓏔	𓏕	𓏖	𓏗	𓏘	𓏙	𓏚	𓏛	𓏜	𓏝	𓏞	𓏟
# U+133Ex	𓏠	𓏡	𓏢	𓏣	𓏤	𓏥	𓏦	𓏧	𓏨	𓏩	𓏪	𓏫	𓏬	𓏭	𓏮	𓏯
# U+133Fx	𓏰	𓏱	𓏲	𓏳	𓏴	𓏵	𓏶	𓏷	𓏸	𓏹	𓏺	𓏻	𓏼	𓏽	𓏾	𓏿
# U+1340x	𓐀	𓐁	𓐂	𓐃	𓐄	𓐅	𓐆	𓐇	𓐈	𓐉	𓐊	𓐋	𓐌	𓐍	𓐎	𓐏
# U+1341x	𓐐	𓐑	𓐒	𓐓	𓐔	𓐕	𓐖	𓐗	𓐘	𓐙	𓐚	𓐛	𓐜	𓐝	𓐞	𓐟
# U+1342x	𓐠	𓐡	𓐢	𓐣	𓐤	𓐥	𓐦	𓐧	𓐨	𓐩	𓐪	𓐫	𓐬	𓐭	𓐮	𓐯
# Notes
# 1.^ As of Unicode version 15.0
"""
