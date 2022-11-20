from os import system

from colorama import Fore
from numpy import row_stack, array, putmask, char

ESC = '\033'
CSI = ESC + '['


def execute_CSI_code(code: str | int, *args: str | int):
    """Executes an CSI ANSI escape code."""
    print(CSI + "".join([str(arg) + ';' for arg in args]
          [:-1]) + str(code), end='')


def set_title(title: str):
    """Sets the title of the terminal."""
    system(f'title {title}')


class Color:
    auto_reset = True

    NORMAL = Fore.RESET
    DEFAULT = NORMAL
    RESET = NORMAL
    BLACK = Fore.BLACK                     # #000000
    GRAY = Fore.LIGHTBLACK_EX              # #666666
    BRIGHT_WHITE = Fore.LIGHTWHITE_EX      # #E5E5E5

    BRIGHT_RED = Fore.LIGHTRED_EX          # #F14C4C
    RED = Fore.RED                         # #CD3131
    YELLOW = Fore.YELLOW                   # #E5E510
    BRIGHT_YELLOW = Fore.LIGHTYELLOW_EX    # #F5F543
    BRIGHT_GREEN = Fore.LIGHTGREEN_EX      # #23D18B
    GREEN = Fore.GREEN                     # #0DBC79
    CYAN = Fore.CYAN                       # #11A8CD
    BRIGHT_CYAN = Fore.LIGHTCYAN_EX        # #29B8DB
    BRIGHT_BLUE = Fore.LIGHTBLUE_EX        # #3B8EEA
    BLUE = Fore.BLUE                       # #2472C8
    MAGENTA = Fore.MAGENTA                 # #BC3FBC
    BRIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX  # #D670D6


class Cursor:
    pos = (0, 0)

    @classmethod
    def up(cls, n: int = 1) -> None:
        """Moves the cursor `n` cells up."""
        cls.pos = cls.pos[0] - 1, cls.pos[1]
        execute_CSI_code('A', n)

    @classmethod
    def down(cls, n: int = 1) -> None:
        """Moves the cursor `n` cells down."""
        cls.pos = cls.pos[0] + 1, cls.pos[1]
        execute_CSI_code('B', n)

    @classmethod
    def forward(cls, n: int = 1) -> None:
        """Moves the cursor `n` cells forward (right)."""
        cls.pos = cls.pos[0], cls.pos[1] + 1
        execute_CSI_code('C', n)

    @classmethod
    def back(cls, n: int = 1) -> None:
        """Moves the cursor `n` cells back (left)."""
        cls.pos = cls.pos[0], cls.pos[1] - 1
        execute_CSI_code('D', n)

    @classmethod
    def move(cls, pos: tuple[int, int]) -> None:
        cls.pos = pos
        execute_CSI_code('H', *pos)


class Screen:
    @staticmethod
    def clear_line(mode: int | str = 2):
        execute_CSI_code('K', mode)

    @staticmethod
    def clear(mode: int | str = 2):
        Cursor.pos = (0, 0)
        execute_CSI_code('J', mode)

    @staticmethod
    def write(
        txt: object,
        pos: tuple[int, int] = ...,
        color: Color = ...,
        move_cursor: bool = True
    ) -> None:
        txt = str(txt)
        if Color.auto_reset:
            if color is ...:
                color = Color.DEFAULT

        if pos is not ...:
            Cursor.move(pos)
        else:
            height = txt.count('\n')
            width = len(max(txt.split('\n')))
            Cursor.pos = Cursor.pos[0] + height, Cursor.pos[1] + width

        if color is not None:
            print(color, end='')
        print(txt, end='')

        if not move_cursor:
            for _ in range(txt.count('\n') + 1):
                Cursor.up()


class Matrix:
    """Converts a str into a Matrix so it can be easily edited and then returned back to a str.

    ### Uses
    Cell: `[row, column]`
    Rectangular Range: `[row_start : row_end, column_start : column_end]`

    ### Examples
    >>> matrix = ([[12,  5,  2,  4],
    ...            [ 7,  6,  8,  8],
    ...            [ 1,  6,  7,  7]])
    >>> matrix[0, 1]
    5
    # 0 is Implied before the :
    >>> matrix[:2, :3]  # two rows, three columns
    [[12,  5,  2],
     [ 7,  6,  8]]
    >>> matrix[:, 0]  # first column
    [12  7  1]
    >>> matrix[0, :]   # first row
    [12  5  2  4]
    """

    def __init__(self, str_: str, array_=None) -> None:
        if str_[-1] != '\n':
            str_ += '\n'
        self.__str = str_
        if array_ is not None:
            self._matrix = array_
        else:
            self._matrix = row_stack([array(list(row))
                                      for row in self.__str.splitlines(True)])
            # print(self._matrix)

    def __len__(self) -> int:
        return len(self._matrix)

    def __getitem__(self, slice_):
        return self._matrix[slice_]

    def __setitem__(self, slice_, to: str):
        self._matrix[slice_] = to

    def __iter__(self):
        for row in self._matrix:
            yield row

    def __str__(self) -> str:
        """The str formed from the matrix."""
        return "".join([char for row in self._matrix for char in row])

    @property
    def shape(self):
        return self._matrix.shape


class Frame:
    def __init__(self, size: tuple[int, int]) -> None:
        # Convert size to index size
        self.size = (size[0] - 1, size[1] - 1)
        self.height = self.rows + 1
        self.width = self.cols + 1
        # self.inner_size = size[0] - 1, size[1] - 1 # was -1 

        try:
            frame = f'╭{"─" * (self.width - 2)}╮\n'
            for _ in range(self.height - 2):
                frame += f'│{" " * (self.width - 2)}│\n'
            frame += f'╰{"─" * (self.width - 2)}╯\n'
        except:
            print('Invalid frame')

        self.frame = Matrix(frame)

    @property
    def rows(self) -> int:
        return self.size[0]

    @property
    def cols(self) -> int:
        return self.size[1]

    def __getitem__(self, item) -> None:
        return self.frame[item]

    def __setitem__(self, item, to) -> None:
        self.frame[item] = to

    @property
    def top_edge_positions(self) -> list[tuple[int, int]]:
        return [(0, col) for col in range(1, self.cols)]

    @property
    def bottom_edge_positions(self) -> list[tuple[int, int]]:
        return [(self.rows, col) for col in range(1, self.cols)]

    @property
    def left_edge_positions(self) -> list[tuple[int, int]]:
        return [(row, 0) for row in range(1, self.rows)]

    @property
    def right_edge_positions(self) -> list[tuple[int, int]]:
        return [(row, self.cols) for row in range(1, self.rows)]

    @property
    def top_left_corner(self) -> tuple[int, int]:
        return (0, 0)

    @property
    def bottom_left_corner(self) -> tuple[int, int]:
        return (self.rows, 0)

    @property
    def top_right_corner(self) -> tuple[int, int]:
        return (0, self.cols)

    @property
    def bottom_right_corner(self) -> tuple[int, int]:
        return self.size


class MainFrame(Frame):
    def add_frame(
        self,
        frame: Frame,
        pos: tuple[int, int],
    ) -> None:
        # (0, 0)
        top_left = pos
        # (0, 23)
        top_right = (pos[0] + frame.top_right_corner[0],
                     pos[1] + frame.top_right_corner[1]) 
        # (2, 0)
        bottom_left = (pos[0] + frame.bottom_left_corner[0],
                       pos[1] + frame.bottom_left_corner[1])
        
        # (2, 23)
        bottom_right = (pos[0] + frame.bottom_right_corner[0],
                        pos[1] + frame.bottom_right_corner[1])

        if top_left in self.top_edge_positions:
            self.frame[top_left] = '┬'
        elif top_left in self.left_edge_positions:
            self.frame[top_left] = '├'

        if top_right in self.top_edge_positions:
            self.frame[top_right] = '┬'
        elif top_right in self.right_edge_positions:
            self.frame[top_right] = '┤'

        if bottom_left in self.top_edge_positions: # I don't think you want to do this
            self.frame[bottom_left] = '┬'
        elif bottom_left in self.left_edge_positions:
            self.frame[bottom_left] = '├'

        if bottom_right in self.top_edge_positions:
            self.frame[bottom_right] = '┬'
        if bottom_right in self.right_edge_positions:
            self.frame[bottom_right] = '┤'
            # for row in range(bottom_right[1])[1:-1]:
            #     self.frame[(bottom_right[0], row)] = '─'

        # print(pos[0], bottom_left[0], pos[1], bottom_left[1])
        # 0:3, 0
        # x = frame[pos[0]:3, 0:24].copy()
        # print(x)
        # putmask(x, x == " ", frame.frame._matrix)
        """
    
        ╭──────────────────────╮ # I want
        │                 |    │ # want
        │                 |    │ # this
        ╰──────────────────────╯
    ╭──────────────────────╮ # h
    │                      │ # e
    │                      │ # r
    ├                      ┤ # e
    │                      │
    │                      │
    │                      │
    │                      │
    │                      │
    │                      │
    ╰──────────────────────╯╭──────────────────────╮ # I want
                            │                      │ # want
                            │                      │ # this
                            ╰──────────────────────╯
    

            (24 + 5) - width
        """ #(width + pos[1])
            #(height + pos[0]) = 
        # Horizontal
        # pos: 3, width: 6
        #     ------
        # Map, width: 10
        # ----------

        # Vertical map_height - (pos + height)             
        # pos: 3, height: 4        Map, height: 8
        #                           |
        #                           |
        #                           |
        #                           |
        # |                         |
        # |                         |
        # |                         |
        #                           ----
        # 
        # ----------

        # TODO: Fix the problem with frames
        # Vertical position of the frame with height and y coordinate combined.
        frame_vertical_pos = (pos[0] + frame.height) # 8 + 2 = 10 when 11 is max
        frame_horizontal_pos = (pos[1] + frame.width)

        start_row = 1 if pos[0] == 0 else 0
        end_row = frame_vertical_pos - (frame_vertical_pos - self.height + 1) if self.height < frame_vertical_pos else self.height
        start_col = 1 if pos[1] == 0 else 0
        end_col = frame_horizontal_pos - (frame_horizontal_pos - self.width + 1) if self.width < frame_horizontal_pos else self.width 
        # print(frame.frame)
        # print(frame.frame[0:3])
        print(start_row, end_row)
        print(start_col, end_col)
        slc = frame.frame[start_row:end_row, start_col:end_col]
        print(slc)
        for y in range(start_row, len(slc)):
            for x in range(0, len(slc[0])):
                self.frame[y + 1, x + 1] = slc[y, x]


        # self.frame._matrix[(1 if pos[0] == 0 else 0):, (1 if pos[1] == 0 else 0):frame.cols - pos[1] - 1] = slc
        # print(slc)
        # print(self.frame)
        # self.frame._matrix[1:bottom_left[0], 1:-2] = slc
        # print(slc_main)
        # for i in slc:
        #     for j in slc_main
        # print(slc)
        # result = "".join([b if b != " " else a for x in frame.frame._matrix for y in self.frame._matrix[0:bottom_left[0]] for a, b in zip(x, y)])
        # print(result)
        Screen.write(str(Matrix("\n", array_=self.frame)))


x = MainFrame((12, 24))
# print(Frame((3, 24)).frame)
x.add_frame(Frame((4, 22)), (1, 1))
# print(x.frame)

