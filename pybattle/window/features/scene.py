from pybattle.ansi.screen import Screen
from pybattle.window.frames.frame import Frame


class Scene:
    windows: list[Frame] = []
    window = None

    def __init__(self, frame: Frame) -> None:
        self.__window = frame

    @classmethod
    def show(cls, index: int = 0) -> None:
        """Show the current Window.
        
        index: 
        ```
        0 -> first one
        1 -> second one
        -1 -> previous one
        ...
        """
        Screen.clear()
        if cls.window is not None:
            Screen.write(cls.windows[index - 1])
        
    def set(self) -> None:
        """Set the window."""
        Scene.window = self.__window
        Scene.windows.append(Scene.window)

    def set_and_show(self) -> None:
        self.set()
        Scene.show()
