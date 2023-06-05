from pathlib import Path
from time import sleep
from typing import Any, TypeAlias, TypeVar

from pygame import mixer

from pybattle.types_ import BackgroundTask
from pybattle.window.event import Event

mixer.init()


class Sound:
    def __init__(self, file: Path | str) -> None:
        self._sound = mixer.Sound(file)

    def play(self):
        self._sound.play()

    def stop(self):
        self._sound.stop()

    def fade_in(self, time: float = 1, max_volume: int = 100):
        self._sound.set_volume(0)
        self._sound.play()

        def fade_in():
            for i in range(max_volume):
                self._sound.set_volume(i / 100)
                sleep(time / max_volume)

            return 1

        Event(fade_in).start()

    def fade_out(self, time: float = 1):
        def fade_out():
            for i in range(100):
                sleep(time / 100)
                self._sound.set_volume(1 - i / 100)
            self.stop()
            return 1

        Event(fade_out).start()
