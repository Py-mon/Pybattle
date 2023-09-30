from pathlib import Path

# from pygame import mixer

# mixer.init()


class Sound:
    FADE_SECONDS = 3

    def __init__(self, file: Path | str) -> None:
        # self._sound = mixer.Sound(file)
        pass

    # def play(self):
    #     self._sound.play()

    # def stop(self):
    #     self._sound.stop()

    # def fade_in(self, seconds: float = FADE_SECONDS):
    #     self._sound.play(fade_ms=round(seconds * 1000))

    # def fade_out(self, seconds: float = FADE_SECONDS):
    #     self._sound.fadeout(round(seconds * 1000))

    # def set_volume(self, percent: float):
    #     self._sound.set_volume(percent)
