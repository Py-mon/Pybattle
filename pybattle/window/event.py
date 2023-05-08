from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Any, Callable, Generator, Iterator, Self

from keyboard import is_pressed

from window.frames.frame import Frame


class Event:
    events: list[Self] = []
    _executor = ThreadPoolExecutor()

    def __init__(
        self, event: Callable[..., Any], *args: Any, stop_all: bool = False
    ) -> None:
        self._result: Any = None
        self.args = args

        self.stopped = False

        def loop():
            while not self.stopped:
                self._result = event(*self.args)
                if self._result is not None:
                    if stop_all:
                        Event.stop_all()
                    return self._result

        self.loop = loop

        type(self).events.append(self)

    def disable(self):
        """Remove the Event from Event.events"""
        type(self).events.remove(self)

    def finish(self) -> Any:
        """Wait for the Event to finish and return the result"""
        return self.submit.result()

    def start(self):
        """Start running the Event"""
        self.submit = type(self)._executor.submit(self.loop)

    def play(self) -> Any:
        """Start and finish the Event, returning the result"""
        self.start()
        return self.finish()

    @classmethod
    def start_all(cls):
        """Start running all the Events at the same time"""
        for event in cls.events:
            event.start()

    def result(self) -> Any | None:
        """If the Event is done it returns the result otherwise it returns None"""
        if self.submit.done():
            self.disable()
            return self.submit.result()
        else:
            sleep(0.01)

    @classmethod
    def get_next_result(cls) -> Any:
        """Block the main thread and wait for the next result from a Event"""
        return next(cls.results())

    @classmethod
    def results(cls) -> Iterator[Any]:
        """Get the results of the Events"""
        while cls.events:
            for event in cls.events:
                result = event.result()
                if result:
                    yield result

    def stop(self):
        """Finish the current iteration of the Event and stop the next ones"""
        self.stopped = True

    @classmethod
    def stop_all(cls):
        """Stop all the Events"""
        for event in cls.events:
            event.stop()
