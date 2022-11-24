from os import system
from typing import Union, Optional, Self
from colorama import Fore
from numpy import row_stack, array, putmask, char
from src.help import function_info
from src.window.coord import Coordinate
from src.window.matrix import Matrix
from src.window.size import Size


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


class Frame:
    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        *,
        size: Optional[tuple[int, int]]=None
    ) -> None:
        if width is not None and height is not None:
            self._size = Size(width, height)
            print(self._size)
            print(self._size.get_size())
        elif size is not None:
            self._size = Size(size=size)
        else:
            print(f'Incorrectly initialized size. {function_info(self.__init__)}')
            exit(1)
        
        self.initialize_frame_matrix()

    def initialize_frame_matrix(self):
        try:
            init_width = self.width - 2 if self.width - 2 >= 0 else None
            init_height = self.height - 2 if self.height - 2 >= 0 else None
            if init_width is None or init_height is None:
                print('Not full frame created.')
                exit(1)

            frame = f'╭{"─" * (self.width - 2)}╮\n'
            for _ in range(self.height - 2):
                frame += f'│{" " * (self.width - 2)}│\n'
            frame += f'╰{"─" * (self.width - 2)}╯\n'
        except Exception as e:
            print('Invalid frame')
            exit(1)

        self.frame = Matrix(frame)

    # @property
    # def rows(self) -> int:
    #     return self._size.height

    # @property
    # def cols(self) -> int:
    #     return self._size.width

    @property
    def height(self) -> int:
        return self._size.height

    @property
    def width(self) -> int:
        return self._size.width

    @height.setter
    def height(self, new_height: int) -> None:
        self._size.height = new_height

    @width.setter
    def width(self, new_width: int) -> None:
        self._size.width = new_width

    @property
    def size(self) -> tuple[int, int]:
        return self._size.get_size()

    def __getitem__(self, item) -> None:
        return self.frame[item]

    def __setitem__(self, item, to) -> None:
        self.frame[item] = to

    ############ POSITION FUNCTIONS #############
    # P.S. Positions start from 0
    """ TODO: Good improvement would be to create a custom class which is essentialy the list of Coordinates
    Because currently, in add_frame function the 'in' keyword only works like this: top_edge_positions in frame_position
    This is a workaround implemented in the coord.py, Coordinate class, __contains__ method.
    I want it to work like this: frame_position in top_edge_position.
    classname: CoordinatesList(range_x, range_y, ...)

    Also, using CoordinatesList is gonna look much better and more readable in edges functions
    """
    @property 
    def top_edge_positions(self) -> list[tuple[int, int]]:
        """ Get frame's top edge characters positions """

        return [Coordinate(x = x_pos, y = 0) for x_pos in range(1, self.width - 1)]

    @property
    def bottom_edge_positions(self) -> list[tuple[int, int]]:
        """ Get frame's bottom edge characters positions """

        return [Coordinate(x = x_pos, y = self.height - 1) for x_pos in range(1, self.width - 1)]

    @property
    def left_edge_positions(self) -> list[tuple[int, int]]:
        """ Get frame's left edge characters positions """

        return [Coordinate(x = 0, y = y_pos) for y_pos in range(1, self.height - 1)]

    @property
    def right_edge_positions(self) -> list[tuple[int, int]]:
        """ Get frame's right edge characters positions """

        return [Coordinate(x = self.width - 1, y = y_pos) for y_pos in range(1, self.height - 1)]

    @property
    def top_left_corner(self) -> tuple[int, int]:
        return Coordinate(x = 0, y = 0)

    @property
    def bottom_left_corner(self) -> tuple[int, int]:
        return Coordinate(x = 0, y = self.height - 1)

    @property
    def top_right_corner(self) -> tuple[int, int]:
        return Coordinate(x = self.width - 1, y = 0)

    @property
    def bottom_right_corner(self) -> tuple[int, int]:
        return Coordinate(x = self.width - 1, y = self.height - 1)


class MainFrame(Frame):
    # def __init__(
    #     self, 
    #     width: Optional[int] = None, 
    #     height: Optional[int] = None, 
    #     *, 
    #     size: Optional[tuple[int, int]] = None
    # ) -> None:
    #     super().__init__(width, height, size=size)

    def add_frame(
        self,
        frame: Frame,
        x: Optional[int] = None,
        y: Optional[int] = None,
        pos: Optional[Coordinate] = None,
    ) -> None:
        if x is not None and y is not None:
            frame_position = Coordinate(x, y)
        elif pos is not None:
            frame_position = pos
        else:
            print(f'No values passed or they were passed incorrectly. {function_info(self.add_frame)}')
            exit(1)
                
        # Start position (23, 0) - ((1, 1) + (22, 0)) = (23, 0) - (23, 1) = (0, -1) => width
        # if (main_frame.top_right_position.x - (frame_position.x + frame_width)).x <= 0: limit frame width to the main_frame boundaries
        # (0, 11) - ((1, 1) + (0, 12)) = (0, 11) - (1, 13) = (-1, -2) => height
        # if (main_frame.bottom_left_position.y - (frame_position.y + frame_height)).y <= 0: limit frame height ot the main_frame boundaries
        print('Top right corner:', self.top_right_corner)
        print('Frame position:', frame_position)
        print('Frame size:', frame.size)


        out_of_boundaries_step_x = (self.top_right_corner - (frame_position + frame.size)).x
        out_of_boundaries_step_y = (self.bottom_left_corner - (frame_position + frame.size)).y

        print('Coord out of boundaries x:', out_of_boundaries_step_x)
        print('Coord out of boundaries y:', out_of_boundaries_step_y)

        if out_of_boundaries_step_x <= 0:
            limit = 1 if out_of_boundaries_step_x < 0 else abs(out_of_boundaries_step_x) 
            frame.width -= limit

        if out_of_boundaries_step_y <= 0:
            limit = 1 if out_of_boundaries_step_y < 0 else abs(out_of_boundaries_step_y)
            frame.height -= limit

        print('New frame size:', frame.size)
        print(frame.frame)

        top_left = frame_position 
        top_right = frame_position + frame.top_right_corner
        bottom_left = frame_position + frame.bottom_left_corner
        bottom_right = frame_position + frame.bottom_right_corner


        # TODO: Write get_y_x_coords() everywhere is a bit ugly. Needs some refactoring.
        # TODO: Make the character change work not only for edges of the frame but also for the parts of the frame
        # that went out of boundaries.
        if self.top_edge_positions in top_left:
            self.frame[*top_left.get_y_x_coords()] = '┬'
        elif self.left_edge_positions in top_left:
            self.frame[*top_left.get_y_x_coords()] = '├'

        if self.top_edge_positions in top_right:
            self.frame[*top_right.get_y_x_coords()] = '┬'
        elif self.right_edge_positions in top_right:
            self.frame[*top_right.get_y_x_coords()] = '┤'

        if self.bottom_edge_positions in bottom_left:
            self.frame[*bottom_left.get_y_x_coords()] = '┴' # REPLACE THIS ONE WITH REVERSED
        elif self.left_edge_positions in bottom_left:
            self.frame[*bottom_left.get_y_x_coords()] = '├'

        if self.bottom_edge_positions in bottom_right:
            self.frame[*bottom_right.get_y_x_coords()] = '┴' # REPLACE THIS ONE WITH REVERSED
        if self.right_edge_positions in bottom_right:
            self.frame[*bottom_right.get_y_x_coords()] = '┤'

        """
            ##### TO REMOVE #####
        ╭──────────────────────╮ # I want
        │                 |    │ # want
        │                 |    │ # this
        ╰──────────────────────╯
    ╭──────────────────────╮ 0 and 23 coords are borders
    │ x───────────────────╮┤ x at pos (2, 2), frame size = (height: 4, width: 21)
    │ |                    │ Main frame width = 24
    ├ |                    ┤ if pos[1] + frame.width - 1 >= main_width - 1:
    │ |-------             │    main_width - 1 - 
    │                      │ 0 and 10 coords are borders
    │ x─────             | │ x at pos (6, 2) (7), frame height = 4.
    │ |                  | │ Main frame height = 11.
    │ |                  | │ if pos[0] + height - 1 >= main_height - 1: 
    │ |                  | │    10 - (11 - 10)
    ╰──────────────────────╯ else:
                                pos[0] + height - 1


                            ╭──────────────────────╮ # I want
                            │                      │ # want
                            │                      │ # this
                            ╰──────────────────────╯"""


        # start_pos_x = 1 if frame_position.x == 0 else 0
        # start_pos_y = 1 if frame_position.y == 0 else 0 


        # TODO 5: If one of the positions of the frame is 0 then cut the part that overlaps with the border
        # It is needed to make the coordinates inside of the MainFrame
        frame_slice = frame[
            0 : frame_position.y + frame.height,
            0 : frame_position.x + frame.width
        ]

        # frame.height -= start_pos_y
        # frame.width -= start_pos_x
        print(frame_slice)
        for y in range(0, frame.height):
            for x in range(0, frame.width):
                # print(Coordinate(x = x, y = y))

                """ TODO: If the frame with ID is implemented then it solves a lot of problems.
                    - The first one is that we don't need to bother about TODO 5 because we can just check
                    if the character's ID is ID of the MainFrame, so we just skip it
                    - The second is that Frame class becomes easily scalable to maps, zones, etc.
                    Also the drawing of the intersecting frames becomes easier since we need to check if
                    the intersecting frame is not MainFrame and consider special cases like: ╭, ╮, ╯, ╰"""

                if self.frame[y + frame_position.y, x + frame_position.x] == ' ':
                    self.frame[y + frame_position.y, x + frame_position.x] = frame_slice[y, x] 

        Screen.write(str(Matrix("\n", array_=self.frame)))
