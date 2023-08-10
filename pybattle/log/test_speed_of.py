from argparse import ArgumentParser
from cProfile import Profile
from decimal import Decimal
from os import path, walk
from time import sleep
from typing import Self

from keyboard import press_and_release, write

parser = ArgumentParser()

parser.add_argument("file", type=str)
parser.add_argument("--sort", type=str, choices=["cum_time", "time"], default="time")
parser.add_argument("--decimal_places", type=int, default=5)
parser.add_argument("--top_results", type=int, default=1000)
args = parser.parse_args()
code_file = args.file
decimal_places = args.decimal_places
top = args.top_results
sort = args.sort


def find_function_file(function_name, line_number):
    for root, _, files in walk("pybattle"):
        for file in files:
            if file.endswith(".py"):
                file_path = path.abspath(path.join(root, file))
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                if 1 <= line_number <= len(lines):
                    line = lines[line_number - 1]
                    if function_name in line:
                        yield file_path[0].lower() + file_path[1:]
    return None


class Stat:
    def __init__(
        self,
        key: tuple[str, int, str],
        value: tuple[
            int, int, int, int, dict[tuple[str, int, str], tuple[int, int, int, int]]
        ],
    ) -> None:
        line_num = key[1]
        if line_num == 0:
            line_num = None

        _callers = value[4]

        self.method_name = key[2]
        if (
            self.method_name.startswith("<")
            and self.method_name.endswith(">")
            or not self.method_name.islower()
        ):
            self.method_name = None

        self.line_num = line_num
        self.calls = value[1]
        self.cum_time = round(Decimal(value[3]), decimal_places)
        self.time = round(Decimal(value[2]), decimal_places)

        self.file_paths = []

        self.built_in = False
        self.file_path = key[0]
        if self.file_path == "~":
            self.built_in = True
            self.file_path = None
        elif (
            self.file_path.startswith("<")
            and self.file_path.endswith(">")
            and self.method_name is not None
        ):
            self.file_paths = [
                file for file in find_function_file(self.method_name, self.line_num)
            ]
            if len(self.file_paths) != 0:
                self.file_path = self.file_paths[0]
                self.file_paths = self.file_paths[1:]
            else:
                self.file_path = None

        self._callers = _callers

        self.callers = {}

    @property
    def link(self):
        """The link to the method."""
        return (
            f'{self.file_path or ""}{":" if self.line_num else ""}{self.line_num or ""}'
        )

    @property
    def log(self):
        return f"{self.link} ({self.method_name})"

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, Stat):
            return self.log == other.log
        return False


with open(code_file, encoding="utf-8") as file:
    code = file.read()

profile = Profile(builtins=False).run(code)

profile.snapshot_stats()

stats: dict[tuple[str, int, str], Stat] = {
    key: Stat(key, value) for key, value in profile.stats.items()
}


if sort == "cum_time":
    sort = lambda x: x[1].cum_time
else:
    sort = lambda x: x[1].time

stats = dict(sorted(stats.items(), key=sort, reverse=True)[:top])


for stat in stats.values():
    stat.callers = dict(
        sorted(
            {key: stats[key] for key in stat._callers}.items(),
            key=sort,
            reverse=True,
        )
    )

    # for key in stat._callers:
    #     try:
    #         stat.callers[key] = stats[key]
    #     except KeyError:
    #         pass

    # stat.callers = dict(sorted(stat.callers.items(), key=sort, reverse=True))


def find_callers(callers):
    for stat in stats.values():
        for caller in callers:
            if caller == stat:
                for key in stat._callers:
                    stat.callers[key].callers = stats[key].callers
                    find_callers(stats[key].callers)


find_callers(stats.values())


max_calls_len = max([len(str(stat.calls)) for stat in stats.values()])


def format_stats(stats, level, parents):
    indent = (" " * (level * 2)) + "- " if level != 0 else ""
    stats_repr = ""

    for stat in stats.values():
        if stat not in parents:
            if (
                stat.file_path is not None
                and stat.method_name is not None
                and not stat.file_path.startswith("C")
            ):
                stats_repr += f"{indent}{str(stat.calls).zfill(max_calls_len)} {stat.time} {stat.cum_time} {stat.log}\n"

            for file_path in stat.file_paths:
                stats_repr += f'{" " * (len(indent) + max_calls_len + len(str(stat.time)) + len(str(stat.cum_time)) + 3)}{file_path}:{stat.line_num} ({stat.method_name})\n'
            stats_repr += format_stats(stat.callers, level + 1, [stat, *parents])

    return stats_repr


stats_repr = f"Ran {code_file} in {sum([stat.time for stat in stats.values()])} seconds...\n{'Calls'.center(max_calls_len)} {'Time'.center(decimal_places + 2)} {'CumTime'.center(decimal_places + 2)}\n\n"
stats_repr += format_stats(stats, 0, [])


with open("logs/time.log", "w") as f:
    f.write(stats_repr)


def fold(file):
    press_and_release("ctrl+p")

    sleep(0.2)

    write(file, 0.01)

    sleep(0.3)

    press_and_release("enter")

    sleep(0.05)

    press_and_release("ctrl+k+0")


fold("logs/time.log")
