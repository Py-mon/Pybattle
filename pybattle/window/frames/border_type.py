from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from pybattle.window.frames.conjunctions import get_conjunction, Conjunction, Thickness
from pybattle.window.grid.matrix import Cell


class BorderType:
    def __init__(
        self,
        top_right: Conjunction,
        top_left: Conjunction,
        bottom_right: Conjunction,
        bottom_left: Conjunction,
        horizontal: Conjunction,
        vertical: Conjunction,
    ) -> None:
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left
        self.horizontal = horizontal
        self.vertical = vertical
        
    @property
    def top_right_cell(self):
        return Cell(get_conjunction(self.top_right), conjunction=self.top_right)
    
    @property
    def top_left_cell(self):
        return Cell(get_conjunction(self.top_left), conjunction=self.top_left)
    
    @property
    def bottom_right_cell(self):
        return Cell(get_conjunction(self.bottom_right), conjunction=self.bottom_right)
    
    @property
    def bottom_left_cell(self):
        return Cell(get_conjunction(self.bottom_left), conjunction=self.bottom_left)
    
    @property
    def horizontal_cell(self):
        return Cell(get_conjunction(self.horizontal), conjunction=self.horizontal)
    
    @property
    def vertical_cell(self):
        return Cell(get_conjunction(self.vertical), conjunction=self.vertical)
        
    def __repr__(self) -> str:
        return (
            f"{self.top_right_cell}{self.horizontal_cell * 4}{self.top_left_cell}\n"
            f"{self.vertical_cell}    {self.vertical_cell}\n"
            f"{self.bottom_right_cell}{self.horizontal_cell * 4}{self.bottom_left_cell}\n"
        )
        

def _uniform(thickness: Thickness) -> tuple[Conjunction, Conjunction, Conjunction, Conjunction, Conjunction, Conjunction]:
    return {'down': thickness, 'right': thickness}, {'down': thickness, 'left': thickness}, {'up': thickness, 'right': thickness}, {'up': thickness, 'left': thickness}, {'left': thickness, 'right': thickness}, {'up': thickness, 'down': thickness}

    
class Borders:
    """
    ```
    Thin:
        ╭───╮ 
        │   │
        ╰───╯
    Thick:
        ┏━━━┓
        ┃   ┃
        ┗━━━┛
    Double:
        ╔═══╗ 
        ║   ║
        ╚═══╝
    """
    THIN = BorderType(*_uniform('thin'))
    THICK = BorderType(*_uniform('thick'))
    DOUBLE = BorderType(*_uniform('double'))
