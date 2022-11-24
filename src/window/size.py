from typing import Union, Optional

SizeType = Union[list, tuple] # [width, height]; (width, height)

class Size:
    """
    Description: Custom size class for easy size handling.
    class: Size

    Properties:
        width -> int
        height -> int

    Examples:
        size = Size(100, 100)
        print(size) ==> (Width: 100, Height: 100)

    """
    def __init__(
        self,
        width: Optional[int] = None, 
        height: Optional[int] = None,
        *, 
        size: Optional[SizeType] = None
    ) -> None:
        if ((width is not None and height is None) or (height is not None and width is None)) and not size:
            print(f'Only one size attribute was initialized. width:{width}, height:{height}')
            exit(1)


        if width is not None and height is not None:
            self._width = width
            self._height = height
        elif width is not None and size is not None:
            print('Got an ambiguity. You must only pass either size or width and height arguments.')
            exit(1)
        elif width is None and size is not None:
            self._width = size[0]
            self._height = size[1]
        elif width is None and size is None:
            print('Size isn\'t initialized.')
            exit(1)

    @property
    def width(self) -> int:
        return self._width
            
    @width.setter
    def width(self, new_width: int) -> None:
        self._width = new_width

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, new_height: int) -> None:
        self._height = new_height

    def get_size(self) -> SizeType:
        return (self.width, self.height)

    def __repr__(self) -> str:
        return f'(Width: {self.width}, Height: {self.height})'