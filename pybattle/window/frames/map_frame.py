from typing import Optional

from pybattle.window.frames.frame import Frame
from pybattle.window.grid.matrix import Matrix
from pybattle.ansi.colors import Colors, ColorType
from pybattle.window.grid.coord import Coord
from pybattle.window.frames.border_type import BorderType, Borders


class MapFrame(Frame):
    """A text map inside a Frame.
```
╭─ BEDROOM ────────────────────╮
│                   ||||       │
│                   ||||       │
│                     ─┬─┬─┬─┬─│
│                              │
│                              │
│╭│╮   ╶─╮                     │
││││    ░│                     │
│╰│╯   ╶─╯           ╭─────┬─╮ │
│                    │░░░░░│▓│ │
│                    ╰─────┴─╯ │
╰──────────────────────────────╯"""

    def __init__(
        self,
        contents: str,
        title: Optional[str] = None,
        border_color: ColorType = Colors.DEFAULT,
        title_color: ColorType = Colors.DEFAULT,
        border_type: BorderType =  Borders.THIN,
        colors: list[tuple[Coord, ColorType]] = [],
    ) -> None:
        contents_ = Matrix(contents)
        
        self.size = contents_.size + 3

        super().__init__(self.size, title, border_color, title_color, border_type)

        self.contents = contents_
        self.contents.add_colors(*colors)

        self._construct_frame()
