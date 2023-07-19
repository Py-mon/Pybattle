from pybattle.ansi.ansi import AnsiEscSeq
from window.text.grid.point import Coord


class CursorCode:
    """Codes for ANSI escape sequences to move the cursor"""

    UP = "A"
    DOWN = "B"
    LEFT = "C"
    RIGHT = "D"
    MOVE = "H"


class Cursor:
    """Keeps track of the cursor position"""

    pos = Coord(0, 0)

    @classmethod
    def up(cls, n: int = 1) -> None:
        """Move the cursor `n` cells up"""
        cls.pos.y -= 1
        AnsiEscSeq(CursorCode.UP, n - 1).exec()

    @classmethod
    def down(cls, n: int = 1) -> None:
        """Move the cursor `n` cells down"""
        cls.pos.y += 1
        AnsiEscSeq(CursorCode.DOWN, n - 1).exec()

    @classmethod
    def right(cls, n: int = 1) -> None:
        """Move the cursor `n` cells right"""
        cls.pos.x += 1
        AnsiEscSeq(CursorCode.RIGHT, n - 1).exec()

    @classmethod
    def left(cls, n: int = 1) -> None:
        """Move the cursor `n` cells left"""
        cls.pos.x -= 1
        AnsiEscSeq(CursorCode.LEFT, n - 1).exec()

    @classmethod
    def move(cls, pos: Coord) -> None:
        """Move the cursor to the given pos"""
        cls.pos = pos + 1
        AnsiEscSeq(CursorCode.MOVE, *cls.pos).exec()

    @classmethod
    def hide(cls) -> None:
        """Hide the cursor"""
        AnsiEscSeq("?25l").exec()

    @classmethod
    def show(cls) -> None:
        """Show the cursor"""
        AnsiEscSeq("?25h").exec()
