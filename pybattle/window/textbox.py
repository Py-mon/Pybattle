from textwrap import wrap
from time import sleep
from typing import Optional

from keyboard import is_pressed, wait

from pybattle.ansi.colors import Colors
from pybattle.ansi.screen import Cursor, Screen
from pybattle.types_ import SizeReference
from pybattle.window.frame import Frame, Size
from pybattle.window.matrix import Matrix, ColorCoord


class TextBox:
    # TODO: Color Support
    """A outlined box that can display text in the terminal."""
        
    def __init__(
        self,
        text: str = '',
        author: Optional[str] = None,
        size: SizeReference = Size(4, 70),
        alignment: str = 'left',
        block_char: str = '⏷'
    ) -> None:
        self.text = text
        self.size = Size(size)
        self.alignment = alignment
        self.author = author
        
        self.wrap_width = self.size.inner_width - 6  # | x ⏷ |
        self.text_width = self.size.inner_width - 3  # | x |
        self.block = False
        self.block_char = block_char

    def __str__(self) -> str:
        self.textbox = Frame(
            (' ' * self.size.inner_width + '\n') * self.size.inner_height)
        self.textbox.name = self.author

        lines = wrap(self.text, self.wrap_width)[-self.size.inner_height:]  # Last lines
        
        string = ''
        for i in range(self.size.inner_height):
            line = None
            if i <= len(lines) - 1:
                if self.alignment.lower() == 'center':
                    line = f' {lines[i]:^{self.text_width}} \n'
                elif self.alignment.lower() == 'right': 
                    line = f' {lines[i]:>{self.text_width}} \n'
                else:  # left alignment
                    line = f' {lines[i]:<{self.text_width}} \n'

                if self.block and i == len(lines) - 1:
                    line = line[:-3] + self.block_char + line[-2:]
            else:
                line = f' {" ":<{self.text_width}} \n'
                
            string += line

        self.textbox = Frame(Matrix(string, ColorCoord((-3, -1), Colors.BLUE)))

        return str(self.textbox)
    
    def add(self, text: str) -> None:
        """Adds text to the TextBox."""
        self.text += text

    def clear(self) -> None:
        """Clears the TextBox's text."""
        self.text = ''
        
    def refresh(self) -> None:
        Cursor.up(self.size.height + 1).execute()
        print(str(self))

    def speech(
        self,
        text: str = ...,

        default_delay: float = 0.05,
        default_sped_up_delay: float = 0.02,
        delays: dict[str, float] = ...,
        sped_up_delays: dict[str, float] = ...,
        speed_key: str = ' ',

        block: bool = True,
        block_char: str = ...,
        block_key: str = ' ',

        add: bool = False,
        start_clear: bool = False,
        end_clear: bool = False,
    ) -> None:
        """Slowly types out text in the TextBox."""
        if delays is ...:
            delays = {
                '.': 1.00,
                '?': 1.00,
                ';': 0.75,
                ',': 0.50,
                ':': 0.50,
            }
        if sped_up_delays is ...:
            sped_up_delays = {
                '.': 0.50,
                '?': 0.50,
                ';': 0.35,
                ',': 0.25,
                ':': 0.25,
            }
        if text is ...:
            text = self.text
        if block_char is not ...:
            self.block_char = block_char

        if start_clear:
            Screen.clear()
        if not add:
            self.clear()

        lines = wrap(text, self.wrap_width)
        lines = [line.split() for line in lines]

        for index, line in enumerate(lines):
            for word in line:
                if self.block:
                    self.refresh()
                    
                    wait(block_key)
                    self.block = False
                    
                for char in word:
                    self.add(char)
    
                    self.refresh()
                        
                    if is_pressed(speed_key):
                        sleep(sped_up_delays.get(char, default_sped_up_delay))
                    else:
                        sleep(delays.get(char, default_delay))
            
                self.add(' ')
                
            #      If theres fully new display             OR    the last iteration   AND block is True then...
            if ((index - 1) % self.size.inner_height == 0 or index == len(lines) - 1) and block:
                self.block = True

        if end_clear:
            Screen.clear()