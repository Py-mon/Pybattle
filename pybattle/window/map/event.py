from threading import Thread
from time import sleep
from typing import Any, Callable, Never, Union, Generator


class Event:
    _events = []

    def __init__(self, func: Callable[[], Any]) -> None:
        self._result: Any = None

        def loop() -> Union[Never, Any]:
            self._result = func()

        self._func = loop

        type(self)._events.append(self)

    def finish(self) -> Any:
        """Wait for the Event to finish and return the result."""
        self._thread.join()

        self._events.remove(self)

        return self._result

    def start(self) -> None:
        """Start the Event."""
        self._thread = Thread(target=self._func)
        self._thread.start()

    def play(self) -> Any:
        """Start and finish the Event."""
        self.start()
        return self.finish()

    @classmethod
    def gen_all(cls) -> Generator[Any, None, None]:
        """Generate all the Events."""
        for event in cls._events:
            event.start()
        for event in cls._events:
            yield event.finish()

    @classmethod
    def play_all(cls):
        """Play all the Events at the same time."""
        for event in cls._events:
            event.start()
        for event in cls._events:
            event.finish()
