from typing import Optional

from pybattle.window.frames.frame import Frame
from pybattle.window.grid.matrix import Matrix
from pybattle.window.grid.size import Size
from pybattle.types_ import MatrixReference
from pybattle.ansi.colors import Color


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
        contents: MatrixReference,
        title: Optional[str] = None,
        border_color: Optional[Color] = None,
        title_color: Optional[Color] = None,
    ) -> None:
        self.size = Matrix(contents).size + 3
        
        super().__init__(self.size, title, border_color, title_color)

        self.contents = Matrix(contents)
        
        # self.contents.colors += contents.colors
        
        self._update_frame()
