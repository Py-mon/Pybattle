from asyncio import sleep, ensure_future
from enum import Enum


class EventExit(Enum):
    STOP = 0


class Event:
    def __init__(self, func, delay_seconds: float = 0.05) -> None:
        self.func = func
        self.delay_seconds = delay_seconds

    async def _loop(self):
        while True:
            if self.func() == EventExit.STOP:
                break
            await sleep(self.delay_seconds)

    def start(self):
        ensure_future(self._loop())

