from threading import Thread
from typing import Any, Callable, Self, Iterator
from pybattle.window.frames.base_frame import _Frame
from pybattle.debug.log import logger


class Event:
    _events = []

    @classmethod
    def from_frame(cls, frame: _Frame):
        for frame_ in frame.event_frames:
            Event(frame_.event, frame_)

    def __init__(self, event: Callable[..., Any], *args: Any) -> None:
        self._result: Any = None
        self.args = args

        def loop():
            self._result = event(*self.args)

        self._func = loop

        type(self)._events.append(self)

    def finish(self) -> Any:
        """Wait for the Event to finish and return the result"""
        self._thread.join()

        self._events.remove(self)

        return self._result

    def start(self) -> None:
        """Start the Event"""
        self._thread = Thread(target=self._func)
        self._thread.start()

    def play(self) -> Any:
        """Start and finish the Event"""
        self.start()
        return self.finish()

    @classmethod
    def gen_all(cls) -> Iterator[Any]:
        """Generate all the Events"""
        for event in cls._events:
            event.start()
        for event in cls._events:
            yield event.finish()

    @classmethod
    def play_all(cls):
        """Play all the Events at the same time"""
        for event in cls._events:
            event.start()
        for event in cls._events:
            event.finish()
