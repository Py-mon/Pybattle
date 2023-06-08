from cProfile import Profile, _Label
from decimal import Decimal
from time import sleep
from typing import Optional, Self

from keyboard import press_and_release, write


class Stat:
    def __init__(
        self,
        key: _Label,
        value: tuple[int, int, int, int, dict[_Label, tuple[int, int, int, int]]],
    ) -> None:
        line_num = key[1]
        if line_num == 0:
            line_num = None

        _callers = value[4]

        self.method_name = key[2]
        self.line_num = line_num
        self.calls = value[1]
        self.cum_time = float(round(Decimal(value[3]), 5))
        self.time = float(round(Decimal(value[2]), 5))
        self.file_path = key[0]

        self._callers = _callers

        self.callers = {}

    @property
    def name(self):
        return f'{self.file_path or ""}:{self.line_num or ""} {self.method_name}'


code_file = "pybattle/window/frames/frame.py"

with open(code_file) as file:
    code = file.read()

profile = Profile().run(code)

profile.snapshot_stats()


stats: dict[tuple[str, int, str], Stat] = {
    key: Stat(key, value) for key, value in profile.stats.items()
}

stats = dict(sorted(stats.items(), key=lambda x: x[1].time, reverse=True))


for stat in stats.values():
    stat.callers = dict(
        sorted(
            {key: stats[key] for key in stat._callers}.items(),
            key=lambda x: x[1].time,
            reverse=True,
        )
    )


def find_callers(caller):
    for stat in stats.values():
        if stat == caller:
            for key in stat._callers[4]:
                stat.callers[key].callers = stats[key].callers
                find_callers(stats[key].callers)


for stat in stats.values():
    find_callers(stat)


def format_stats(parent, stats, level=0):
    if level > 8:
        return ""

    indent = (" " * (level * 4)) + "- " if level != 0 else ""
    stats_repr = ""

    for stat in stats.values():
        if "<" not in stat.name and parent != stat and not stat.file.startswith("C"):
            stats_repr += (
                f"{indent}{stat.calls} {stat.time} {stat.cum_time} {stat.name}\n"
            )
        stats_repr += format_stats(stat, stat.callers, level + 1)

    return stats_repr


stats_repr = f"In {sum([stat.time for stat in stats.values()])}\n"
stats_repr += format_stats(None, stats)


with open("logs/time.log", "w") as f:
    f.write(stats_repr)


def fold(file):
    press_and_release("ctrl+p")

    sleep(0.1)

    write(file, 0.01)

    sleep(0.1)

    press_and_release("enter")

    sleep(0.1)

    press_and_release("ctrl+k+0")


fold("logs/time.log")
