from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum
from threading import Lock
from time import sleep
from typing import Any, Callable, Iterator, Optional


class EventExit(Enum):
    Silent = 0


lock = Lock()


class Event:
    _executor = ThreadPoolExecutor()
    _events = []

    def __init__(
        self,
        event: Callable[[], Any],
    ) -> None:
        self._result: Any = None
        self.event = event

        self.stopped = False

        type(self)._events.append(self)

    @classmethod
    def stop_all(cls):
        for event in cls._events:
            event.stop()

    @classmethod
    def play_all(cls):
        for event in cls._events:
            event.play()

    def _loop(self):
        lock.acquire()
        while not self.stopped:
            self._result = self.event()

            if self._result is not None:
                self.stopped = True
                return self._result
        lock.release()

    def finish(self) -> Any:
        """Wait for the Event to finish and return the result"""
        return self.submit.result()

    def start(self):
        """Start running the Event"""
        self.submit = type(self)._executor.submit(self._loop)

    def play(self) -> Any:
        """Start and finish the Event, returning the result (blocks)"""
        self.start()
        return self.finish()

    def stop(self):
        """Finish the current iteration of the Event and stop the next ones"""
        self.stopped = True


class EventGroup:
    def __init__(
        self, *events: Callable[[], Any], init: Optional[Callable[[], None]] = None
    ) -> None:
        self.events = [Event(event) for event in events]
        self.init = init

    def stop(self):
        for event in self.events:
            event.stop()

    def results(self) -> Iterator:
        if self.init is not None:
            self.init()

        for event in self.events:
            event.start()

        for future in as_completed([event.submit for event in self.events]):
            result = future.result()

            if result == EventExit.Silent:
                continue

            # todo: stop the event

            if isinstance(result, Exception):
                raise result
            yield result

    def get_next_result(self) -> Any:
        """Block the main thread and wait for the next result from a Event"""
        return next(self.results())

    def play(self):
        for result in self.results():
            self.stop()

            return result  # ?


def print_x_every_5_seconds():
    while True:
        print("x")
        sleep(5)


def print_y_every_1_second():
    while True:
        pass


def main():
    task1 = Event(print_x_every_5_seconds())
    task2 = Event(print_y_every_1_second())
    task2.start()
    task1.start()
    


main()
