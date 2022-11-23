from typing import Union, Optional, Self

PositionType = Union[list, tuple] # ([x, y], (x, y))

class Coordinate:
    """
    Description: Class to store the 2D coordinate. And all the manipulations with it and more.
    class: Coordinate
    Properties:
        x -> int
        y -> int

    Examples:
        c1 = Coordinate(1, 2)
        c2 = Coordinate(2, 3)
        c1.x = 10
        c1.y = 11
        print(c1)                   ==> (x: 10, y: 11)
        print(*c1)                  ==> 10, 11
        print(c1.get_coords())      ==> (10, 11)
        print(c1.get_y_x_coords())  ==> (11, 10)
        c3 = c1 + c2 ==> Coordinate(x = 12, y = 14)
        c3 = c1 - c2 ==> Coordinate(x = 8, y = 8)
        print(c1 == c2)             ==> False
        c1 = Coordinate(2, 3)
        print(c1 == c2)             ==> True
        c3 += (c1 + c2)             ==> Coordinate(x = 12, y = 14)
    """
    def __init__(
        self, 
        x: Optional[int] = None,
        y: Optional[int] = None,
        *,
        position: Optional[PositionType] = None
    ) -> None:
        # Only one coordinate cannot be intialized
        # Being paranoic here
        if ((x is not None and y is None) or (y is not None and x is None)) and not position:
            print(f'Only one coordinate was initialized. x:{x}, y:{y}')
            exit(1)

        if x is not None and y is not None:
            self._x = x
            self._y = y
        elif x is not None and position is not None:
            print('Got an ambiguity. You must only pass either position or x and y coords.')
            exit(1)
        elif x is None and position is not None:
            self._x = position[0]
            self._y = position[1]
        elif x is None and position is None:
            print('[WARNING]: Coordinates are not set. Initialized to: (0, 0)')
            self._x = 0
            self._y = 0

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, new_x: int) -> None:
        self._x = new_x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, new_y: int) -> None:
        self._y = new_y

    def get_coords(self) -> tuple[int, int]:
        return (self.x, self.y)

    def get_y_x_coords(self):
        return (self.y, self.x)


    # TODO: Improve those functions by making Self | PositionType a separate Union.
    # TODO: Also maybe think of a way to refactor isinstance methods and make them reusable (Creating a type checking class is not a bad idea)
    def add(self, other: Self | PositionType) -> Self:
        """ Adds 2 coordinates """
        new_coords = Coordinate()
        if isinstance(other, Coordinate):
            new_coords.x = self.x + other.x
            new_coords.y = self.y + other.y
        elif isinstance(other, PositionType) and len(other) == 2: # Passing only x, y
            # print('here')
            new_coords.x = self.x + other[0]
            new_coords.y = self.y + other[1]
        return new_coords

    def subtract(self, other: Self | PositionType) -> Self:
        """ Subtract the second coordinate from the first """
        new_coords = Coordinate()
        if isinstance(other, Coordinate):
            new_coords.x = self.x - other.x
            new_coords.y = self.y - other.y
        elif isinstance(other, PositionType) and len(other) == 2:
            new_coords.x = self.x - other[0]
            new_coords.y = self.y - other[1]
        return new_coords

    def __add__(self, other: Self | PositionType) -> Self:
        return self.add(other)

    def __iadd__(self, other: Self | PositionType) -> Self:
        return self.add(other)

    def __sub__(self, other: Self | PositionType) -> Self:
        return self.subtract(other)

    def __isub__(self, other: Self | PositionType) -> Self:
        return self.subtract(other)

    def __iter__(self) -> tuple:
        """TODO: ['_x', '_y'] is a current hack to get a correct order of returning.
           Make it variable name and order independent. For example:
           if we have attributes y, _x so it should return [_x, y]
        """ 
        return (self.__dict__[coord] for coord in ['_x', '_y']) 

    def __eq__(self, other: Self | PositionType) -> bool:
        if isinstance(other, Coordinate):
            if self.x == other.x and self.y == other.y:
                return True
        elif isinstance(other, PositionType) and len(other) == 2:
            if self.x == other[0] and self.y == other[1]:
                return True

        return False

    # Workaround
    # TODO: Also add contains for lists of tuples and lists of lists
    def __contains__(self, sequence: list[Self]) -> bool:
        for coord in sequence:
            if self.x == coord.x and self.y == coord.y:
                return True
        return False

    def __repr__(self) -> str:
        return f'(x: {self.x}, y: {self.y})'