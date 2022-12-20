from textwrap import wrap
from typing import Optional

from pybattle.ansi.color import Colors
from pybattle.window.frame import Frame
from pybattle.window.frame import Size
from pybattle.types_ import SizeReference
from pybattle.ansi.screen import Screen, Cursor
from time import sleep
from keyboard import is_pressed, wait


class TextBox:
    """A outlined box that can display text in the terminal."""
        
    def __init__(
        self,
        text: str = '',
        author: Optional[str] = None,
        size: SizeReference = Size(4, 70),
        alignment: str = 'left',
    ) -> None:
        self.text = text
        self.size = Size.convert_reference(size)
        self.alignment = alignment
        self.author = author
        
        self.wrap_width = self.size.inner_width - 6  # | x ⏷ |
        self.text_width = self.size.inner_width - 3  # | x |

    def __str__(self) -> str:
        self.textbox = Frame(
            (' ' * self.size.inner_width + '\n') * self.size.inner_height)
        self.textbox.name = self.author

        lines = wrap(self.text, self.wrap_width)[-self.size.inner_height:]  # Last lines
        
        string = ''
        for i in range(self.size.inner_height):
            if i <= len(lines) - 1:
                if self.alignment.lower() == 'center':
                    string += f' {lines[i]:^{self.text_width}} \n'
                elif self.alignment.lower() == 'right': 
                    string += f' {lines[i]:>{self.text_width}} \n'
                else:  # left alignment
                    string += f' {lines[i]:<{self.text_width}} \n'
            else:
                string += f' {" ":<{self.text_width}} \n'
        
        self.textbox = Frame(string)
        
        return str(self.textbox)
    
    def add(self, text: str) -> None:
        """Adds text to the TextBox."""
        self.text += text

    def clear(self) -> None:
        """Clears the TextBox's text."""
        self.text = ''

    def speech(
        self,
        text: str = ...,

        default_delay: float = 0.05,
        default_sped_up_delay: float = 0.02,
        delays: dict[str, float] = ...,
        sped_up_delays: dict[str, float] = ...,
        speed_key: str = ' ',

        block: bool = True,
        block_char: str = '⏷',
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
        if text == ...:
            text = self.text
        else:
            if '\\' in text:
                raise ValueError("text must not include any '\\'")

        if start_clear:
            Screen.clear()
        if not add:
            self.clear()

        lines = wrap(text, self.wrap_width)

        sped = False
        for index, line in enumerate(lines):

            for char in line:
                self.add(char)

                Cursor.up(self.size.height + 1).execute()
                print(str(self))

                if char == block_char:
                    wait(block_key)
                    self.text = self.text.replace('⏷', '', -1)
                    
                if is_pressed(speed_key):
                    sped = True
                else:
                    sped = False
                    
                if sped:
                    sleep(sped_up_delays.get(char, default_sped_up_delay))
                else:
                    sleep(delays.get(char, default_delay))
        if end_clear:
            Screen.clear()


print(TextBox("In Ancient Egyptian architecture, the sun was often used as a symbol of the concept of ma'at, which roughly translates as 'truth, justice, and balance.' This was reflected in the design of many ancient Egyptian buildings, which were often oriented to face the rising sun in the east. For example, temples were often built with their main entrances facing the east, and many tombs were also oriented in this direction. In addition, the sun was often depicted in various forms throughout ancient Egyptian architecture, including as a disc with rays emanating from it, as a falcon-headed god, or as the solar boat that carried the god Ra across the sky. These representations of the sun were meant to invoke the power and majesty of the divine and to remind people of the importance of living in accordance with the principles of ma'at.").speech())
            # #      If theres fully new display             OR    the last iteration   AND block is True then...
            # if ((index + 1) % self.size.inner_height == 0 or index == len(lines) - 1) and block:
            #     line += ' ' + block_char
            # else:
            #     line += ' '    