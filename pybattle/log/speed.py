from argparse import ArgumentParser
from cProfile import run, Profile
from pstats import SortKey, Stats

parser = ArgumentParser()

parser.add_argument("file", type=str)
code_file = parser.parse_args().file


with open(code_file) as file:
    code = file.read()
    


run(code, "logs/time.log")



# Takes the binary file and translates it into text in time.log
with open("logs/time.log", "a") as file:
    stats = Stats("logs/time.log", stream=file)

    file.truncate(0)

    stats.sort_stats(SortKey.TIME)

    stats.print_callers()


new = ""
with open("logs/time.log") as file:
    last_start = 0
    last_end = 0
    for i, line in enumerate(file.readlines()[4:-3]):
        start = line.index("  ")
        if start == 0:
            new += "    - " + line[132:]
            continue

        replacement = line[start : line.index("<") - 1]
        if len(replacement) != 0:
            new += "\n" + line.replace(replacement, "\n ")

with open("logs/time.log", "w") as file:
    file.write(new)
